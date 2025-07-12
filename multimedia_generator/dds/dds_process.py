import colorsys
from pathlib import Path
import imageio.v3 as iio
import numpy as np
from PIL import Image

from multimedia_generator import utils, constants


def process_dds(dds_file_path: Path):
    dds_image = iio.imread(dds_file_path)
    image = Image.fromarray(dds_image)
    r_tint, g_tint, b_tint = constants.icon_color

    # Convert image to NumPy array
    img_array = np.array(image, dtype=np.uint8)

    # Extract color and alpha channels
    r, g, b, alpha = img_array[..., 0], img_array[..., 1], img_array[..., 2], img_array[..., 3]

    # Find fully transparent pixels (alpha == 0)
    transparent_mask = (alpha < 255)

    if np.any(transparent_mask):  # Check if there are transparent pixels to process
        # Compute grayscale luminance using the common formula
        luminance = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)

        # Normalize luminance to [0, 1] range
        luminance_norm = luminance / 255.0 * 2

        # Apply tint while keeping luminance
        img_array[transparent_mask, 0] = (luminance_norm[transparent_mask] * r_tint).astype(np.uint8)  # Red
        img_array[transparent_mask, 1] = (luminance_norm[transparent_mask] * g_tint).astype(np.uint8)  # Green
        img_array[transparent_mask, 2] = (luminance_norm[transparent_mask] * b_tint).astype(np.uint8)  # Blue
        img_array[transparent_mask, 3] = 255  # Make tinted pixels fully visible

    # Convert back to image and save
    result = Image.fromarray(img_array, "RGBA")
    return result


if __name__ == '__main__':
    image_path = constants.AOE_UNIT_ICONS_FOLDER / "048_50730.DDS"
    image1 = process_dds(image_path)
    image1.show()
