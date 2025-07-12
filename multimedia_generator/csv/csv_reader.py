from pathlib import Path

from multimedia_generator.csv.csv_model import CSVUnitGif, CSVUnitIcon


def read_csv_unit_gif(file_path: Path) -> list[CSVUnitGif]:
    units = []
    with file_path.open('r') as f:
        lines = [line.strip().split(';') for line in f if not line.startswith('#')]
        for items in lines:
            unit_id = int(items[0])
            image = items[1]
            animations = items[2]
            ok = items[3] == "1"
            csv_object = CSVUnitGif(unit_id, image, animations, ok)
            units.append(csv_object)
    return units


def read_csv_unit_icon(file_path: Path) -> list[CSVUnitIcon]:
    units = []
    with file_path.open('r') as f:
        lines = [line.strip().split(';') for line in f if not line.startswith('#')]
        for items in lines:
            unit_id = int(items[0])
            image = items[1]
            csv_object = CSVUnitIcon(unit_id, image)
            units.append(csv_object)
    return units
