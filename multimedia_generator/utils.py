import math
from io import BytesIO

from PIL import Image

from multimedia_generator import constants

PLAYER_COLOR_MAP = {
    "blue": lambda x: [(y := x * 1.8) - 384, y - 255, y],
    "red": lambda x: [(y := x * 1.8), y - 255, y - 255],
    "green": lambda x: [(y := x * 1.44) - 255, y, y - 255],
    "yellow": lambda x: [(y := x * 1.5), y, y - 255],
    "cyan": lambda x: [(y := x * 1.5) - 255, y, y],
    "purple": lambda x: [(y := x * 1.6), y - 255, y],
    "gray": lambda x: [x, x, x],
    "orange": lambda x: [(y := x * 1.8), y * .5, y - 255]
}


def read_string_from_bytes(file_stream: BytesIO, num_bytes: int) -> str:
    return file_stream.read(num_bytes).decode('utf-8')


def read_bytes(file_stream: BytesIO, num_bytes: int, signed=False) -> int:
    return int.from_bytes(file_stream.read(num_bytes), byteorder="little", signed=signed)


def read_chunk(file_stream: BytesIO) -> BytesIO:
    size = read_bytes(file_stream, 4, signed=False)
    real_size = (size - 1) >> 2 << 2  # align to 4 bytes
    stream = BytesIO(file_stream.read(real_size))
    stream.seek(0)
    return stream


def from_color_16(color_value: int):
    return [
        (color_value >> 11 & 0x1F) * 255 / 31,
        (color_value >> 5 & 0x3F) * 255 / 63,
        (color_value & 0x1F) * 255 / 31
    ]


def to_color_16(color):
    return round(color[0] * 31 / 255) << 11 | round(color[1] * 63 / 255) << 5 | round(color[2] * 31 / 255)


def mix_value(value0, value1, value) -> int:
    return int(math.floor(value0 * (1 - value) + value1 * value))


def mix_colors(color0: list, color1: list, value: float) -> list[int]:
    return [
        mix_value(color0[0], color1[0], value),
        mix_value(color0[1], color1[1], value),
        mix_value(color0[2], color1[2], value)
    ]


def clamp(value, min_value, max_value):
    return min(max_value, max(min_value, value))


def set_image_pixel(image_data: any, offset: int, color: list, alpha: int = 255) -> None:
    offset *= 4
    if color:
        image_data[offset] = color[0]
        image_data[offset + 1] = color[1]
        image_data[offset + 2] = color[2]
        image_data[offset + 3] = alpha


def circular_shift(lst, shift):
    shift %= len(lst)  # Handle shifts larger than the list size
    return lst[shift:] + lst[:shift]


def update_image_limits(limits: list[int | None], coordinates: list[int | None] | None, offset: tuple[int, int] | None = None) -> list[int | None]:
    if coordinates is not None:
        if coordinates[0] is not None and (limits[0] is None or coordinates[0] < limits[0]):
            limits[0] = coordinates[0]
            if offset is not None and offset[0] < 0:
                limits[0] += offset[0]
        if coordinates[1] is not None and (limits[1] is None or coordinates[1] < limits[1]):
            limits[1] = coordinates[1]
            if offset is not None and offset[1] < 0:
                limits[1] += offset[1]
        if coordinates[2] is not None and (limits[2] is None or coordinates[2] > limits[2]):
            limits[2] = coordinates[2]
            if offset is not None and offset[0] > 0:
                limits[2] += offset[0]
        if coordinates[3] is not None and (limits[3] is None or coordinates[3] > limits[3]):
            limits[3] = coordinates[3]
            if offset is not None and offset[1] > 0:
                limits[3] += offset[1]
    return limits


def image_crop_resize(image: Image, limits: list[int | None]) -> Image:
    new_image = Image.new("RGBA", constants.gif_size, (0, 0, 0, 0))
    crop_image = image.crop((limits[0], limits[1], limits[2], limits[3]))
    crop_image.thumbnail(constants.gif_size)
    x_offset = (constants.gif_size[0] - crop_image.width) // 2
    y_offset = (constants.gif_size[1] - crop_image.height) // 2
    new_image.paste(crop_image, (x_offset, y_offset))
    return new_image


class Singleton(type):
    """Metaclass for implementing Singleton pattern."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
