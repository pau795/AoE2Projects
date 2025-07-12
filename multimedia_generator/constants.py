from pathlib import Path

# Base Paths
BASE_PATH = Path("C:/")
DATA_PATH = Path("D:/")

# Age of Empires II Paths
AOE_FOLDER_PATH = BASE_PATH / "Program Files (x86)" / "Steam" / "steamapps" / "common" / "AoE2DE"

# Game Data Files
AOE_DAT_FILE_PATH = AOE_FOLDER_PATH / "resources" / "_common" / "dat" / "empires2_x2_p1.dat"
AOE_DRS_FOLDER_PATH = AOE_FOLDER_PATH / "resources" / "_common" / "drs" / "graphics"

# Strings file
AOE_STRINGS_FILE_PATH = AOE_FOLDER_PATH / "resources" / "en" / "strings" / "key-value" / "key-value-strings-utf8.txt"

# Textures & UI Folders
AOE_INGAME_FOLDER = AOE_FOLDER_PATH / "widgetui" / "textures" / "ingame"
AOE_MENU_FOLDER = AOE_FOLDER_PATH / "widgetui" / "textures" / "menu"

# Icon Categories
AOE_UNIT_ICONS_FOLDER = AOE_INGAME_FOLDER / "units"
AOE_BUILDING_ICONS_FOLDER = AOE_INGAME_FOLDER / "buildings"
AOE_TECH_ICONS_FOLDER = AOE_INGAME_FOLDER / "tech"
AOE_CIV_ICONS_FOLDER = AOE_MENU_FOLDER / "civs"

# Project Folders
# DATABASE_FOLDER = DATA_PATH / "Users" / "pau_7" / "IdeaProjects" / "AoE2DatabaseData"
DATABASE_FOLDER = DATA_PATH / "Proyectos" / "AoE2DatabaseData"
MULTIMEDIA_GENERATOR_FOLDER = DATA_PATH / "Proyectos" / "PythonModels" / "multimedia_generator"

DATABASE_UNIT_LIST = DATABASE_FOLDER / "unit_list.xml"
DATABASE_STRINGS = DATABASE_FOLDER / "en" / "strings.xml"

# Input Paths
INPUT_FOLDER = MULTIMEDIA_GENERATOR_FOLDER / "input"
GIF_INPUT_FOLDER = INPUT_FOLDER / "gifs"
ICONS_INPUT_FOLDER = INPUT_FOLDER / "icons"

# Input Files
GIF_INPUT_UNITS_FILE = GIF_INPUT_FOLDER / "units.csv"
GIF_INPUT_BUILDINGS_FILE = GIF_INPUT_FOLDER / "building_list.xml"

ICONS_INPUT_UNITS_FILE = ICONS_INPUT_FOLDER / "units.csv"
ICONS_INPUT_BUILDINGS_FILE = ICONS_INPUT_FOLDER / "buildings.csv"
ICONS_INPUT_TECH_FILE = ICONS_INPUT_FOLDER / "techs.csv"
ICONS_INPUT_CIVS_FILE = ICONS_INPUT_FOLDER / "civs.csv"

# Output Paths
OUTPUT_FOLDER = MULTIMEDIA_GENERATOR_FOLDER / "output"
GIF_OUTPUT_FOLDER = OUTPUT_FOLDER / "gif_test"
ICONS_OUTPUT_FOLDER = OUTPUT_FOLDER / "icons"

# GIF Output Paths
GIF_OUTPUT_UNITS_FOLDER = GIF_OUTPUT_FOLDER / "units"
GIF_OUTPUT_BUILDINGS_FOLDER = GIF_OUTPUT_FOLDER / "buildings"

# Icons Output Paths
ICONS_OUTPUT_UNITS_FOLDER = ICONS_OUTPUT_FOLDER / "units"
ICONS_OUTPUT_BUILDINGS_FOLDER = ICONS_OUTPUT_FOLDER / "buildings"
ICONS_OUTPUT_TECH_FOLDER = ICONS_OUTPUT_FOLDER / "techs"
ICONS_OUTPUT_CIVS_FOLDER = ICONS_OUTPUT_FOLDER / "civs"


default_civ = 1
default_color = "blue"
uhd_graphics = False
icon_color = [0, 64, 128]
gif_size = (200, 150)
minimum_frame_duration = 20
speed = 1.7
