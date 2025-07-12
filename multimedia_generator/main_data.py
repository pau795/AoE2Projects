from multimedia_generator import constants
from multimedia_generator.dat.dat_reader import DatReader
from multimedia_generator.strings import aoe_string_file_reader
from multimedia_generator.xml import xml_reader


if __name__ == '__main__':
    database_unit_list = xml_reader.read_entity_list_file(constants.DATABASE_UNIT_LIST)
    database_strings = xml_reader.read_string_file(constants.DATABASE_STRINGS)
    game_strings = aoe_string_file_reader.read_lang_file(constants.AOE_STRINGS_FILE_PATH)
    game_data_reader = DatReader()

    name_2_id = {}
    database_id2unit = {}
    for database_unit in database_unit_list:
        name = database_strings[f'unit_name_{database_unit}']
        name_2_id[name] = database_unit
        database_id2unit[database_unit.id] = database_unit 

