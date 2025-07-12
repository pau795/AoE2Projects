from pathlib import Path
import xml.etree.ElementTree as ET

from multimedia_generator.xml.xml_model import DatabaseUnit


def read_entity_list_file(file_path: Path) -> list[DatabaseUnit]:
    xml_file = ET.parse(file_path)
    root = xml_file.getroot()
    unit_list = []
    for unit in root.findall('item'):
        unit_id = unit.get('id') if unit.get('id') is not None else -1
        image = unit.get('image')
        gif_image = f'g_{image}[2:]'
        database_unit = DatabaseUnit(unit_id, -1, "", image, gif_image)
        unit_list.append(database_unit)
    return unit_list


def read_string_file(file_path: Path) -> dict[str, str]:
    string_dict = {}
    xml_file = ET.parse(file_path)
    root = xml_file.getroot()
    for string in root.findall('string'):
        string_dict[string.get('name')] = string.text
    return string_dict
