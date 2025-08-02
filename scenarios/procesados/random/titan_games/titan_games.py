from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.datasets.players import PlayerId
from AoE2ScenarioParser.datasets.trigger_lists import ObjectAttribute
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.objects.support.area import Area
from scenarios.lib.parser_project import ParserProject


class TitanGames(ParserProject):
    def __init__(self,input_scenario_name: str, output_scenario_name: str):
        super().__init__(input_scenario_name, output_scenario_name)

    def process(self):
        unit_manager = self.scenario.unit_manager
        map_manager = self.scenario.map_manager
        trigger_manager = self.scenario.trigger_manager
        player_manager = self.scenario.player_manager
        trigger_data = self.scenario.actions.load_data_triggers()
        xs_manager = self.scenario.xs_manager
        xs_manager.add_script(xs_file_path="timer.xs")

        area_map: Area = trigger_data.areas['map'][0]

        gates = trigger_data.objects['gates']
        magyar_huszar = trigger_data.objects['magyar_huszar'][0]
        villagers = trigger_data.objects['villagers']

        unit_dict = {}

        trigger_dict = {}
        triggers_not_copied = [
            0, 2, 4, 5, 23, 25, 28, 29, 42, 43, 44, 45, 46, 49, 48, 53, 55, 58, 59, 60,
            61, 64, 65, 68, 73, 76, 78, 82, 86, 92, 93, 102, 104, 114, 115, 117, 136, 137, 138,
        ]

        animal_dict = {
            PlayerId.TWO: UnitInfo.KOMODO_DRAGON.ID,
            PlayerId.THREE: UnitInfo.JAGUAR.ID,
            PlayerId.FOUR: UnitInfo.LION.ID,
            PlayerId.FIVE: UnitInfo.SNOW_LEOPARD.ID,
            PlayerId.SIX: UnitInfo.TIGER.ID,
            PlayerId.SEVEN: UnitInfo.RABID_WOLF.ID
        }
        corpse_dict = {
            PlayerId.TWO: 1136,
            PlayerId.THREE: 813,
            PlayerId.FOUR: 1030,
            PlayerId.FIVE: 1242,
            PlayerId.SIX: 1138,
            PlayerId.SEVEN: 237
        }

        flipada_dict = {
            UnitInfo.BEAR.ID: animal_dict,
            489: corpse_dict
        }

        player_one = player_manager.players[PlayerId.ONE]
        for player in [PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN]:
            player_object = player_manager.players[player]
            player_object.disabled_units = player_one.disabled_units.copy()
            player_object.disabled_buildings = player_one.disabled_buildings.copy()
            player_object.disabled_techs = player_one.disabled_techs.copy()
            player_object.civilization = player_one.civilization
            player_object.lock_civ = player_one.lock_civ

        for tile in area_map.to_coords(as_terrain=True):
            for i, player in enumerate(
                    [PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN]):
                new_tile = map_manager.get_tile(tile.x + area_map.get_width() * (i + 1), tile.y)
                new_tile.terrain_id = tile.terrain_id
                new_tile.elevation = tile.elevation
                new_tile.layer = tile.layer

        units = unit_manager.get_units_in_area(x1=area_map.x1, y1=area_map.y1, x2=area_map.x2, y2=area_map.y2)
        for unit in units:
            for i, player in enumerate(
                    [PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN]):

                new_player = player if unit.player != PlayerId.EIGHT and unit.player != PlayerId.GAIA else unit.player
                new_unit = unit_manager.add_unit(
                    player=new_player,
                    unit_const=unit.unit_const,
                    x=unit.x + area_map.get_width() * (i + 1),
                    y=unit.y,
                    z=unit.z,
                    rotation=unit.rotation,
                    status=unit.status)
                if unit.unit_const == UnitInfo.BEAR.ID:
                    new_unit.unit_const = flipada_dict[unit.unit_const][player]
                if unit in gates or unit == magyar_huszar or unit in villagers:
                    if unit.reference_id not in unit_dict:
                        unit_dict[unit.reference_id] = {player: new_unit.reference_id}
                    else:
                        unit_dict[unit.reference_id][player] = new_unit.reference_id

        triggers_to_copy = [trigger.trigger_id for trigger in trigger_manager.triggers
                            if trigger.trigger_id not in triggers_not_copied]

        for init_trigger_id in triggers_to_copy:
            trigger_dict[init_trigger_id] = {}
            for player in [PlayerId.TWO, PlayerId.THREE, PlayerId.FOUR, PlayerId.FIVE, PlayerId.SIX, PlayerId.SEVEN]:
                new_trigger = trigger_manager.copy_trigger(
                    trigger_select=init_trigger_id, append_after_source=False, add_suffix=False
                )
                new_trigger.name = f'{new_trigger.name} (p{player.value})'
                trigger_dict[init_trigger_id][player] = new_trigger.trigger_id

        # 34- 50
        for init_trigger_id, player_dict in trigger_dict.items():
            for (i, (player, new_trigger_id)) in enumerate(player_dict.items()):
                new_trigger = trigger_manager.get_trigger(new_trigger_id)
                for condition in new_trigger.conditions:
                    if condition.area_x1 != -1 or condition.area_x2 != -1:
                        condition.area_x1 = condition.area_x1 + area_map.get_width() * (i + 1)
                        condition.area_x2 = condition.area_x2 + area_map.get_width() * (i + 1)
                    if condition.source_player != -1:
                        new_source_player = player if (condition.source_player != PlayerId.EIGHT and
                                                       condition.source_player != PlayerId.GAIA) else condition.source_player
                        condition.source_player = new_source_player
                    if condition.target_player != -1:
                        new_target_player = player if (condition.target_player != PlayerId.EIGHT and
                                                       condition.target_player != PlayerId.GAIA) else condition.target_player
                        condition.target_player = new_target_player
                    if condition.unit_object in unit_dict:
                        condition.unit_object = unit_dict[condition.unit_object][player]
                    if condition.object_list == UnitInfo.BEAR.ID:
                        condition.object_list = animal_dict[player]
                for effect in new_trigger.effects:
                    if effect.area_x1 != -1 or effect.area_x2 != -1:
                        effect.area_x1 = effect.area_x1 + area_map.get_width() * (i + 1)
                        effect.area_x2 = effect.area_x2 + area_map.get_width() * (i + 1)
                    if effect.location_x != -1:
                        effect.location_x = effect.location_x + area_map.get_width() * (i + 1)
                    if effect.source_player != -1:
                        new_source_player = player if (effect.source_player != PlayerId.EIGHT and
                                                       effect.source_player != PlayerId.GAIA) else effect.source_player
                        effect.source_player = new_source_player
                    if effect.target_player != -1:
                        new_target_player = player if (effect.target_player != PlayerId.EIGHT and
                                                       effect.target_player != PlayerId.GAIA) else effect.target_player
                        effect.target_player = new_target_player
                    if effect.object_list_unit_id == UnitInfo.BEAR.ID:
                        effect.object_list_unit_id = animal_dict[player]
                        if effect.object_attributes == ObjectAttribute.DEAD_UNIT_ID or effect.object_attributes == ObjectAttribute.BLOOD_UNIT:
                            effect.quantity = flipada_dict[effect.quantity][player]
                    if "Jugador 1" in effect.message:
                        effect.message = effect.message.replace("Jugador 1", f'Jugador {player.value}')
                    if effect.effect_type == EffectId.SCRIPT_CALL:
                        effect.message = f'get_time_{player.value}()'
                    if effect.effect_type == EffectId.DISPLAY_TIMER:
                        effect.message = f'Tiempo restante Jugador {player.value} : %d'
                        effect.timer = player.value
                    if effect.effect_type == EffectId.CLEAR_TIMER:
                        effect.timer = player.value
                    new_object_id_list = []
                    for object_id in effect.selected_object_ids:
                        if object_id in unit_dict:
                            new_object_id_list.append(unit_dict[object_id][player])
                        else:
                            new_object_id_list.append(object_id)
                    effect.selected_object_ids = new_object_id_list
                    if effect.trigger_id != -1:
                        effect.trigger_id = trigger_dict[effect.trigger_id][player]

        for init_trigger_id in triggers_to_copy[::-1]:
            init_trigger = trigger_manager.get_trigger(init_trigger_id)
            init_trigger.name = f'{init_trigger.name} (p{PlayerId.ONE.value})'


titan = TitanGames(
    input_scenario_name='The_titan_games',
    output_scenario_name='The_titan_games_output'
)
titan.convert()
