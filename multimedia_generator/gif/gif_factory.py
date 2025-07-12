from pathlib import Path

from PIL import Image

from multimedia_generator.dat.dat_model import GraphicData, UnitData
from multimedia_generator.dat.dat_reader import DatReader
from multimedia_generator.sld import sld_reader
from multimedia_generator import constants, utils


class GIFFactory:

    def __init__(self):
        self.dat_reader = DatReader()

    def create_gif(self, unit_data: UnitData, graphic_data: GraphicData, destination_path: Path) -> None:
        if graphic_data is None:
            return
        images, limits = self.generate_images(constants.AOE_DRS_FOLDER_PATH / graphic_data.sprite_file)
        for delta in graphic_data.deltas:
            delta_graphic = self.dat_reader.get_graphic_data(delta.graphic_id)
            if delta_graphic is None:
                continue
            delta_images, delta_limits = self.generate_images(constants.AOE_DRS_FOLDER_PATH / delta_graphic.sprite_file)
            offset = (delta.offset_x, delta.offset_y)
            if not images and delta_images:
                images = delta_images
                limits = utils.update_image_limits(limits, delta_limits, offset)
            elif delta_images:
                images = [self.composite_images(image, delta_image, offset) for image, delta_image in zip(images, delta_images)]
                limits = utils.update_image_limits(limits, delta_limits, offset)
        duration = max(graphic_data.frame_duration * 1000, constants.minimum_frame_duration)
        if graphic_data.frames_per_angle == 1:
            duration = 500
        if len(images) > 0:
            images = [utils.image_crop_resize(image, limits) for image in images]
            images = utils.circular_shift(images, 4 * graphic_data.frames_per_angle)
            images[0].save(destination_path, save_all=True, append_images=images[1:], optimize=True, duration=duration, loop=0, trasparency=0, disposal=2)

    @staticmethod
    def generate_images(sld_path: Path) -> tuple[list[Image], list[int | None]]:
        if not sld_path.exists():
            return [], [None, None, None, None]
        sprite = sld_reader.read_sprite_file(sld_path)
        images = []
        global_limits = [None, None, None, None]
        for i, frame in enumerate(sprite.frames):
            image, limits = sld_reader.frame_to_image(frame, constants.default_color)
            global_limits = utils.update_image_limits(global_limits, limits)
            images.append(image)
        return images, global_limits

    @staticmethod
    def composite_images(image1: Image, image2: Image, offset) -> Image:
        temp_layer = Image.new("RGBA", image1.size, (0, 0, 0, 0))
        temp_layer.paste(image2, offset)
        return Image.alpha_composite(image1, temp_layer)

