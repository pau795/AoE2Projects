from pathlib import Path
from PIL import Image
from tree_dict import tree_dict


def replicate_image(image_path: Path, rows: int, columns: int):
    # Load original image
    img = Image.open(image_path)
    w, h = img.size

    # Correct canvas size: width = w * columns, height = h * rows
    grid = Image.new("RGBA", (w * columns, h * rows))

    # Paste image copies
    for row in range(rows):
        for col in range(columns):
            grid.paste(img, (col * w, row * h))

    return grid


base_tree = Path('C:\\Users\\pau_7\\Desktop\\trees1\\template\\base_tree.png')
base_felled_tree = Path('C:\\Users\\pau_7\\Desktop\\trees1\\template\\base_felled_tree.png')
output_dir = Path('C:\\Users\\pau_7\\Desktop\\trees1\\output\\')

generated_templates = set()
for tree_object in tree_dict:
    tree_type = tree_object["type"]
    angle_count = tree_object["angle_count"]
    template = (tree_type, angle_count)
    if template not in generated_templates:
        generated_templates.add(template)
        match tree_type:
            case "tree":
                replicate_image(base_tree, 1, angle_count).save(output_dir / f"tree_template_{angle_count}.png")
            case "felled":
                replicate_image(base_felled_tree, 1, angle_count).save(output_dir / f"felled_tree_template_{angle_count}.png")

