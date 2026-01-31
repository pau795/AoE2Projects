import logging
import re
from httpx import RequestError
from nicegui import ui, app
import httpx
import asyncio
from draft_model import DraftModel, Turn, ActionType, PlayerType

draft_pattern = "https://aoe2cm.net/draft/{id}"
draft_api_pattern = "https://aoe2cm.net/api/draft/{id}"


class DraftViewerApp:
    """Handles the NiceGUI interface."""

    round_options = {
        "round_1": "Round 1",
        "round_2": "Round 2",
        "round_3": "Round 3",
        "3rd/4th": "3rd / 4th Placement",
        "finals": "Grand Finals"
    }
    image_size = "96px"
    normal_font_size = "1.5vh"
    small_font_size = "1vh"
    score_font_size = "3.5vh"
    title_font_size = "4vh"
    image_border_size = "0.5vh"

    def __init__(self):
        self.title = ""
        self.civilization_draft_id = ""
        self.map_draft_id = ""
        self.civ_draft: DraftModel | None = None
        self.map_draft: DraftModel | None = None
        self.selected_round = "round_1"
        self.score_host = 0
        self.score_guest = 0

        app.add_static_files("/civ_icons", "data/civ_icons")
        app.add_static_files("/map_icons", "data/map_icons")
        app.add_static_files("/images", "data/images")

        ui.add_head_html('''
        <style>
            .force-object-unset img {
                object-fit: unset !important;
            }             
            .nicegui-content {
                padding: 0 !important;                
            }               
            .q-page-container{
                background-image: url(/images/background-1.png);
                background-size: cover;
                background-position: center;
                width: 100%;        
                font-family: Helvetica;        
            }
        </style>
        ''')

        self.settings_dialog = ui.dialog()
        # Create UI elements once
        with ui.column().classes("w-full items-stretch p-4"):
            with ui.row().classes('relative items-center w-full'):
                self.tittle_label = ui.label("Dynamic Battle Season 3").classes("absolute left-1/2 -translate-x-1/2 font-bold mx-auto").style(f"font-size: {self.title_font_size}")
                ui.button(icon="settings", on_click=self.open_settings_dialog).classes("ml-auto").style(f"font-size: {self.normal_font_size}")
            with ui.element('div').classes('grid grid-cols-3 auto-rows-auto gap-4').style(f"font-size: {self.normal_font_size}"):
                # Row 1
                with ui.element('div').classes('flex flex-col items-end gap-2'):  # host civs
                    self.host_civs_panel = ui.column().classes('flex-1 items-end gap-2')

                with ui.element('div').classes('flex flex-col items-stretch justify-start gap-2'):  # admin scoreboard+civs
                    self.scoreboard_panel = ui.column().classes('items-stretch justify-start gap-2')
                    self.admin_civs_panel = ui.column().classes('flex-grow items-stretch justify-end gap-2')

                with ui.element('div').classes('flex flex-col items-start gap-2'):  # guest civs
                    self.guest_civs_panel = ui.column().classes('flex-1 items-start gap-2')

                # Row 2
                with ui.element('div').classes('flex flex-col items-end gap-2'):  # host maps
                    self.host_maps_panel = ui.column().classes('flex-1 items-end gap-2')

                with ui.element('div').classes('flex flex-col items-stretch justify-start gap-2'):  # admin maps
                    self.admin_maps_panel = ui.column().classes('flex-1 items-stretch justify-start gap-2')

                with ui.element('div').classes('flex flex-col items-start gap-2'):  # guest maps
                    self.guest_maps_panel = ui.column().classes('flex-1 items-start gap-2')

        with self.admin_civs_panel:
            with ui.column().classes("justify-center items-center"):
                ui.space().classes("h-[64px]")
                ui.icon("edit_calendar").classes("text-[256px]")
                ui.label("Waiting for drafts...").classes("font-bold text-xl text-center")
                ui.spinner().classes("text-[96px] text-center")

        ui.timer(0, self.initial_load_cache, once=True)

    @staticmethod
    async def fetch_drafts(civilization_draft_url: str, map_draft_url: str):
        """Fetch data from both endpoints concurrently."""
        async with httpx.AsyncClient() as client:
            resp1, resp2 = await asyncio.gather(
                client.get(civilization_draft_url),
                client.get(map_draft_url),
            )
            if resp1.status_code != 200 or resp2.status_code != 200:
                raise RequestError("Failed to fetch draft data")
        return resp1.json(), resp2.json()

    @staticmethod
    async def save_to_local_storage(key: str, value: str) -> None:
        await ui.run_javascript(f'localStorage.setItem("{key}", "{value}")')

    @staticmethod
    async def read_from_local_storage(key: str, default_value: str = '') -> str:
        """Read a string from localStorage, return default if not found"""
        result = await ui.run_javascript(f"localStorage.getItem('{key}');", timeout=5.0)
        return default_value if result is None else result

    async def clear_cache(self):
        await self.save_to_local_storage("title", "")
        await self.save_to_local_storage("civ_draft", "")
        await self.save_to_local_storage("map_draft", "")
        await self.save_to_local_storage("score_host", "")
        await self.save_to_local_storage("score_guest", "")
        await self.save_to_local_storage("selected_round", "")
        await ui.run_javascript("location.reload();")

    async def initial_load_cache(self):
        title = await self.read_from_local_storage("title", "")
        civilization_draft_id = await self.read_from_local_storage("civ_draft", "")
        map_draft_id = await self.read_from_local_storage("map_draft", "")
        selected_round = await self.read_from_local_storage("selected_round", "round_1")
        score_host = await self.read_from_local_storage("score_host", "0")
        score_guest = await self.read_from_local_storage("score_guest", "0")
        if civilization_draft_id and map_draft_id:
            civilization_draft_url = draft_pattern.replace("{id}", civilization_draft_id) if civilization_draft_id else ""
            map_draft_url = draft_pattern.replace("{id}", map_draft_id) if map_draft_id else ""
            await self.load_draft(title, civilization_draft_url, map_draft_url, selected_round, int(score_host), int(score_guest))

    async def load_draft(self, title: str, civilization_draft: str, map_draft: str, selected_round: str = "round_1", score_host: int = 0, score_guest: int = 0):
        try:
            civ_draft_id = self.match_url(draft_pattern, civilization_draft)
            map_draft_id = self.match_url(draft_pattern, map_draft)
            if not civ_draft_id:
                ui.notify("Invalid Civilization Draft link", color="negative")
                return
            if not map_draft_id:
                ui.notify("Invalid Map Draft link", color="negative")
                return
            if score_host < 0 or score_guest < 0:
                ui.notify("Invalid score", color="negative")
                return
            civilization_draft_url = draft_api_pattern.replace("{id}", civ_draft_id)
            map_draft_url = draft_api_pattern.replace("{id}", map_draft_id)
            civ_draft, map_draft = await self.fetch_drafts(civilization_draft_url, map_draft_url)
            self.civ_draft = DraftModel.from_dict(civ_draft)
            self.map_draft = DraftModel.from_dict(map_draft)
            self.civ_draft.set_admin_civilizations(selected_round)
            self.map_draft.set_admin_maps(selected_round)
            self.score_host = score_host
            self.score_guest = score_guest
            self.selected_round = selected_round
            await self.save_to_local_storage("selected_round", selected_round)
            await self.save_to_local_storage("civ_draft", civ_draft_id)
            await self.save_to_local_storage("map_draft", map_draft_id)
            await self.save_to_local_storage("score_host", str(score_host))
            await self.save_to_local_storage("score_guest", str(score_guest))
            self.map_draft_id = map_draft_id
            self.civilization_draft_id = civ_draft_id
            if title:
                await self.save_to_local_storage("title", title)
                self.title = title
                self.tittle_label.set_text(self.title)
            else:
                await self.save_to_local_storage("title", "")
                self.title = ""
                self.tittle_label.set_text(f"Dynamic Battle Season 3 - {self.round_options[selected_round]}")
            score = f'{score_host} - {score_guest}'
            self.fill_draft_layout(self.civ_draft, self.map_draft, selected_round, score)
            self.settings_dialog.close()
        except Exception as e:
            ui.notify(f"Error: {e}", color="negative")
            logging.exception(e)

    def fill_draft_layout(self, civ_draft: DraftModel, map_draft: DraftModel, selected_round: str = "round_1", score: str = "0 - 0"):
        self.scoreboard_panel.clear()
        self.host_civs_panel.clear()
        self.host_maps_panel.clear()
        self.admin_civs_panel.clear()
        self.admin_maps_panel.clear()
        self.guest_civs_panel.clear()
        self.guest_maps_panel.clear()

        with self.host_civs_panel:
            # ui.label(f"{civ_draft.host_name}").classes("font-bold text-xl !text-blue-500 ms-2")
            with ui.column().classes('flex-grow p-4 gap-2 items-end dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"CIVILIZATION PICKS").classes("font-bold")
                with ui.row().classes('w-full justify-end items-center'):
                    for turn in civ_draft.host_picks:
                        self.create_civ_draft_item(turn)
                ui.space()
                ui.label(f"CIVILIZATION BANS").classes("font-bold")
                with ui.row().classes('w-full justify-end items-center'):
                    for turn in civ_draft.host_bans:
                        self.create_civ_draft_item(turn)

        with self.host_maps_panel:
            with ui.column().classes('flex-grow p-4 gap-2 items-end dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"HOME MAPS").classes("font-bold")
                with ui.row().classes('w-full justify-end items-center'):
                    for turn in map_draft.host_picks:
                        self.create_map_draft_item(turn)
                ui.space()
                ui.label(f"MAP BANS").classes("font-bold")
                with ui.row().classes('w-full justify-end items-center'):
                    for turn in map_draft.host_bans:
                        self.create_map_draft_item(turn)

        # with self.image_panel:
        #     ui.image("/images/dynamic_logo.png").classes('object-scale-down')
        with self.scoreboard_panel:
            with ui.column().classes('p-4 gap-0 items-stretch justify-center dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                with ui.row().classes('flex-grow justify-between items-center').style(f"font-size: {self.score_font_size}"):
                    ui.label(f"{civ_draft.host_name}").classes("flex-1 font-bold !text-red-500 text-center")
                    ui.label(f"{score}").classes("flex-1 font-bold text-center")
                    ui.label(f"{civ_draft.guest_name}").classes("flex-1 font-bold !text-blue-500 text-center")
                with ui.row().classes('w-full justify-center items-center').style(f"font-size: {self.normal_font_size}"):
                    match selected_round:
                        case "round_1" | "round_2" | "round_3":
                            text_format = "Play all 3"
                        case "3rd/4th" | "finals":
                            text_format = "Best of 5"
                    ui.label(text_format).classes("font-bold text-center")

        with self.admin_civs_panel:
            with ui.column().classes('p-4 gap-2 items-center justify-center dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"ADMIN CIVILIZATION BANS").classes("font-bold")
                with ui.row().classes('w-full justify-center items-center'):
                    for turn in civ_draft.admin_bans:
                        self.create_civ_draft_item(turn)

        with self.admin_maps_panel:
            with ui.column().classes('flex-grow p-4 gap-2 items-center justify-center dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"FIRST MAP").classes("font-bold")
                with ui.row().classes('w-full justify-center items-center'):
                    for turn in map_draft.admin_picks:
                        self.create_map_draft_item(turn)
                if map_draft.admin_bans:
                    ui.space()
                    ui.label(f"ADMIN MAP BANS").classes("font-bold")
                    with ui.row().classes('w-full justify-center items-center'):
                        for turn in map_draft.admin_bans:
                            self.create_map_draft_item(turn)

        with self.guest_civs_panel:
            # ui.label(f"{civ_draft.guest_name}").classes("font-bold text-xl !text-red-500 me-2")
            with ui.column().classes('flex-grow p-4 gap-2 items-start dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"CIVILIZATION PICKS").classes("font-bold")
                with ui.row().classes('w-full justify-start items-center'):
                    for turn in civ_draft.guest_picks:
                        self.create_civ_draft_item(turn)
                ui.space()
                ui.label(f"CIVILIZATION BANS").classes("font-bold")
                with ui.row().classes('w-full justify-start items-center'):
                    for turn in civ_draft.guest_bans:
                        self.create_civ_draft_item(turn)

        with self.guest_maps_panel:
            with ui.column().classes('flex-grow p-4 gap-2 items-start dark:bg-gray-800/80 bg-gray-200/80 rounded-lg'):
                ui.label(f"HOME MAPS").classes("font-bold")
                with ui.row().classes('w-full justify-start items-center'):
                    for turn in map_draft.guest_picks:
                        self.create_map_draft_item(turn)
                ui.space()
                ui.label(f"MAP BANS").classes("font-bold")
                with ui.row().classes('w-full justify-start items-center'):
                    for turn in map_draft.guest_bans:
                        self.create_map_draft_item(turn)

    def open_settings_dialog(self):
        self.settings_dialog.clear()
        civilization_draft_url = draft_pattern.replace("{id}", self.civilization_draft_id) if self.civilization_draft_id else ""
        map_draft_url = draft_pattern.replace("{id}", self.map_draft_id) if self.map_draft_id else ""

        with self.settings_dialog, ui.card().classes("items-stretch w-200 max-w-200"):
            ui.label('Settings').classes("font-bold text-xl text-center")
            round_selector = ui.radio(value=self.selected_round, options=self.round_options).props("inline").classes("flex justify-center")
            with ui.row().classes("justify-center"):
                def validate_numeric_input(e):
                    # Get the input element
                    input_element = e.sender
                    # Update the input value with the cleaned number
                    input_element.value = int(e.value) if e.value else 0
                score_host = ui.number("Host Score", min=0, step=1, max=5, value=float(self.score_host), on_change=lambda e: validate_numeric_input(e)).classes("w-30")
                score_guest = ui.number("Guest Score", min=0, step=1, max=5, value=float(self.score_guest), on_change=lambda e: validate_numeric_input(e)).classes("w-30")
            title_input = ui.input('Custom Draft Title', value=self.title).tooltip("Leave this field empty for default title")
            civilization_draft_input = ui.input('Civilization Draft Link', value=civilization_draft_url)
            map_draft_input = ui.input('Map Draft Link', value=map_draft_url)
            with ui.row().classes('mt-4'):
                ui.button("Clear Cache", on_click=self.clear_cache).classes("self-start")
                ui.space()
                ui.button('Cancel', on_click=self.settings_dialog.close)
                ui.button('Save', on_click=lambda: self.load_draft(title_input.value.strip(), civilization_draft_input.value, map_draft_input.value, round_selector.value, int(score_host.value), int(score_guest.value)))
        self.settings_dialog.open()

    def create_civ_draft_item(self, turn: Turn) -> ui.element:
        color = "red" if turn.action == ActionType.BAN else "green" if turn.action == ActionType.PICK else "gray"
        if turn.sniped:
            color = "gray"
        card = ui.column().classes(f'border-solid border-{color}-700 rounded-lg hover:border-{color}-300').style(f"border-width: {self.image_border_size}")
        with card:
            if turn.chosen_option:
                player = "p2" if turn.player == PlayerType.HOST else "p1" if turn.player == PlayerType.GUEST else "p0"
                civ_icon = f'{turn.chosen_option}_{player}.png'
                # Container for the image with relative positioning
                with ui.element('div').classes('relative aspect-square').style(f'width: {self.image_size}'):
                    image_classes = 'w-full h-full force-object-unset'
                    if turn.sniped:
                        image_classes += ' filter grayscale'
                    ui.image(f"/civ_icons/{civ_icon}").classes(image_classes)
                    with ui.element('div').classes('absolute bottom-0 left-0 right-0 bg-black/80 text-white text-center py-1').style(f"font-size: {self.normal_font_size}"):
                        ui.label(f"{turn.chosen_option.title()}")
                    if turn.sniped:
                        # Overlay image (adjust the path and positioning as needed)
                        ui.image("/images/snipe-marker.svg").classes('absolute top-0 left-0 w-full h-full')

                    crown_image = ui.image("/images/crown.svg").classes('absolute top-0 left-0 w-full h-full').style("display: none;")
                    skull_image = ui.image("/images/skull.svg").classes('absolute top-0 left-0 w-full h-full').style("display: none;")

                    crown_visible = False
                    skull_visible = False

                    # tooltip
                    if turn.action == ActionType.PICK and not turn.sniped:
                        with ui.row().classes("absolute bottom-full left-1/2 transform -translate-x-1/2 -translate-y-1 bg-white-200 dark:bg-gray-600 rounded shadow-lg z-50 flex items-center justify-center w-full").style("display: none;") as tooltip:
                            def toggle_crown():
                                nonlocal crown_visible, skull_visible
                                if crown_visible:
                                    crown_image.style("display: none;")
                                    crown_visible = False
                                else:
                                    crown_image.style("display: flex;")
                                    crown_visible = True
                                if skull_visible:
                                    skull_image.style("display: none;")
                                    skull_visible = False

                            def toggle_skull():
                                nonlocal skull_visible, crown_visible
                                if skull_visible:
                                    skull_image.style("display: none;")
                                    skull_visible = False
                                else:
                                    skull_image.style("display: flex;")
                                    skull_visible = True
                                if crown_visible:
                                    crown_image.style("display: none;")
                                    crown_visible = False

                            ui.button(icon='', on_click=toggle_crown).props('flat color=white').classes('w-8 h-8 text-xl').props(f'icon=img:/images/crown.svg')
                            ui.button(icon='', on_click=toggle_skull).props('flat color=white').classes('w-8 h-8 text-xl').props(f'icon=img:/images/skull.svg')
                        card.on('mouseenter', lambda: tooltip.style("display: flex;"))
                        card.on('mouseleave', lambda: tooltip.style("display: none;"))

        return card

    def create_map_draft_item(self, turn: Turn) -> ui.element:
        color = "red" if turn.action == ActionType.BAN else "green" if turn.action == ActionType.PICK else "gray"
        card = ui.column().classes(f'border-solid border-{color}-700 rounded-lg hover:border-{color}-300').style(f"border-width: {self.image_border_size}")
        with card:
            if turn.chosen_option:
                map_icon = f'{turn.chosen_option.lower().replace(" ", "_")}.jpg'
                # Container for the image with relative positioning
                with ui.element('div').classes('relative aspect-square').style(f'width: {self.image_size}'):
                    ui.image(f"/map_icons/{map_icon}").classes("w-full h-full force-object-unset")
                    with ui.element('div').classes('absolute bottom-0 left-0 right-0 bg-black/80 text-white text-center py-1').style(f"font-size: {self.normal_font_size}"):
                        ui.label(f"{turn.chosen_option.title()}")

                    crown_image = ui.image("/images/crown.svg").classes('absolute top-0 left-0 w-full h-full').style("display: none;")
                    skull_image = ui.image("/images/skull.svg").classes('absolute top-0 left-0 w-full h-full').style("display: none;")

                    crown_visible = False
                    skull_visible = False

                    # tooltip
                    if turn.action == ActionType.PICK and not turn.sniped:
                        with ui.row().classes("absolute bottom-full left-1/2 transform -translate-x-1/2 -translate-y-1 bg-white-200 dark:bg-gray-600 rounded shadow-lg z-50 flex items-center justify-center w-full").style("display: none;") as tooltip:
                            def toggle_crown():
                                nonlocal crown_visible, skull_visible
                                if crown_visible:
                                    crown_image.style("display: none;")
                                    crown_visible = False
                                else:
                                    crown_image.style("display: flex;")
                                    crown_visible = True
                                if skull_visible:
                                    skull_image.style("display: none;")
                                    skull_visible = False

                            def toggle_skull():
                                nonlocal skull_visible, crown_visible
                                if skull_visible:
                                    skull_image.style("display: none;")
                                    skull_visible = False
                                else:
                                    skull_image.style("display: flex;")
                                    skull_visible = True
                                if crown_visible:
                                    crown_image.style("display: none;")
                                    crown_visible = False

                            ui.button(icon='', on_click=toggle_crown).props('flat color=white').classes('w-8 h-8 text-xl').props(f'icon=img:/images/crown.svg')
                            ui.button(icon='', on_click=toggle_skull).props('flat color=white').classes('w-8 h-8 text-xl').props(f'icon=img:/images/skull.svg')
                        card.on('mouseenter', lambda: tooltip.style("display: flex;"))
                        card.on('mouseleave', lambda: tooltip.style("display: none;"))
        return card

    @staticmethod
    def match_url(template: str, url: str):
        # Escape all regex characters except our placeholders
        regex = re.escape(template)
        # Replace {id} with a capture group for anything except '/'
        regex = regex.replace(r"\{id\}", r"(?P<id>[^/]+)")
        # Anchor it to match the full string
        regex = f"^{regex}$"

        match = re.match(regex, url)
        if match:
            return match.group("id")
        return None


def main():
    DraftViewerApp()
    ui.run(title="Dynamic Battle LAN Draft Viewer", reload=False, native=False, dark=True, port=7000)


if __name__ == "__main__":
    main()
