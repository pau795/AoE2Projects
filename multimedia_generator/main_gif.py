from pathlib import Path

from multimedia_generator import constants
from multimedia_generator.constants import p2_color
from multimedia_generator.dat.dat_reader import DatReader
from multimedia_generator.gif.gif_factory import GIFFactory
import multimedia_generator.xml.xml_reader as xml_reader
import multimedia_generator.csv.csv_reader as csv_reader
import multimedia_generator.dds.dds_process as dds_processor
from multimedia_generator.sld import sld_reader


class MultimediaGenerator:

    def __init__(self):
        # self.dat_reader = DatReader()
        # self.gif_factory = GIFFactory()
        pass

    def generate_unit_gifs(self):
        csv_items = csv_reader.read_csv_unit_gif(constants.GIF_INPUT_UNITS_FILE)
        for item in csv_items:
            if item.ok:
                continue
            unit_data = self.dat_reader.get_unit_data(item.id)
            graphic = unit_data.attack_graphic if item.animation == "attack" else unit_data.walking_graphic if item.animation == "walking" else unit_data.standing_graphic
            self.gif_factory.create_gif(unit_data, graphic, constants.GIF_OUTPUT_UNITS_FOLDER / f'{item.image}.gif')
            print(f"Unit {unit_data.id} processed, gif {constants.GIF_OUTPUT_UNITS_FOLDER / f'{item.image}.gif'} created")

    def generate_unit_gif(self, unit_id: int):
        unit_data = self.dat_reader.get_unit_data(unit_id)
        graphic = unit_data.attack_graphic
        self.gif_factory.create_gif(unit_data, graphic, constants.GIF_OUTPUT_UNITS_FOLDER / f'{unit_id}.gif')
        print(f"Unit {unit_data.id} processed, gif {constants.GIF_OUTPUT_UNITS_FOLDER / f'{unit_id}.gif'} created")

    def generate_building_gifs(self):
        pass

    def generate_unit_icons(self, file_path: Path):
        csv_items = csv_reader.read_csv_unit_icon(file_path)
        for item in csv_items:
            # unit_data = self.dat_reader.get_unit_data(item.id)
            for dds_image in constants.AOE_UNIT_ICONS_FOLDER.iterdir():
                if dds_image.name.startswith(f'{item.icon:03d}'):
                    for player, color in zip(["p0"], [constants.p0_color]):
                        image = dds_processor.process_dds(dds_image, color)
                        image_name = f'{item.civ}_{player}.png'
                        image.save(Path("C:\\Users\\pau_7\\Desktop\\civ_icons") / image_name)
                        print(f"Unit {item.id} processed, icon ID {item.icon}, original icon {dds_image.name}, {image_name} created")


if __name__ == '__main__':
    generator = MultimediaGenerator()
    # generator.generate_unit_gif(359)
    # generator.generate_unit_gifs()
    # generator.generate_unit_icons(constants.ICONS_INPUT_UNITS_FILE)
    generator.generate_unit_icons(Path("C:\\Users\\pau_7\\Desktop\\civ ids.csv"))





