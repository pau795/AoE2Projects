from pathlib import Path
from PIL import Image


def replicate_image(image_path: Path, rows: int, columns: int):
    # Load original image
    """
    Replicates an image in a grid.

    Args:
        image_path (Path): Path to the image file.
        rows (int): Number of rows in the grid.
        columns (int): Number of columns in the grid.

    Returns:
        Image: A PIL Image object with the replicated image.
    """
    img = Image.open(image_path)
    w, h = img.size
    grid = Image.new("RGBA", (w * columns, h * rows))
    for row in range(rows):
        for col in range(columns):
            grid.paste(img, (col * w, row * h))

    return grid


base_image = Path('base_tree.png')
number_of_frames = 5
output_image_name = "output.png"
replicate_image(base_image, 1, number_of_frames).save(output_image_name)



