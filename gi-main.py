import os
import requests
import json
import time
import logging

# Base URLs
base_url = "https://api.hakush.in/gi/data/"
base_url_v2 = "https://api.hakush.in/v2/gi/data/"
languages = ["zh", "en", "ja", "ko"]

# List of main JSON files to download
main_files = [
    "character.json",
    "weapon.json",
    "artifact.json",
    "monster.json",
    "tower.json",
    "rolecombat.json",
]
main_files_v2 = [
    "gcg.json",
    "furniture.json",
    "suite.json"
]

# Directory to save the files
save_dir = "./gi/data"
save_dir_v2 = "./v2/gi/data"

# Create the save directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
if not os.path.exists(save_dir_v2):
    os.makedirs(save_dir_v2)

# Set up logging
logger = logging.getLogger()
logger.setLevel('DEBUG')
BASIC_FORMAT = "%(asctime)s >> %(levelname)s - %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()
chlr.setFormatter(formatter)
chlr.setLevel('INFO')
fhlrd = logging.FileHandler("./gi-app-debug.log", encoding='utf-8')
fhlrd.setFormatter(formatter)
fhlri = logging.FileHandler("./gi-app-info.log", encoding='utf-8')
fhlri.setFormatter(formatter)
fhlrd.setLevel('DEBUG')
fhlri.setLevel('INFO')
logger.addHandler(chlr)
logger.addHandler(fhlrd)
logger.addHandler(fhlri)

def download_file(url, save_path):
    try:
        response = requests.get(url)
    except Exception as e:
        download_file(url, save_path)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"Successfully downloaded {save_path}")
    else:
        logger.error(f"Failed to download {save_path} with status code {response.status_code}")

# Download new.json
download_file('https://api.hakush.in/gi/new.json', os.path.join(save_dir, "../new.json"))
download_file('https://api.hakush.in/v2/gi/new.json', os.path.join(save_dir_v2, "../new.json"))

# Download main JSON files
for file in main_files:
    url = base_url + file
    save_path = os.path.join(save_dir, file)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    download_file(url, save_path)

for file in main_files_v2:
    url = base_url_v2 + file
    save_path = os.path.join(save_dir_v2, file)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    download_file(url, save_path)

# Download item.json for each language
for lang in languages:
    url = f"{base_url}{lang}/item.json"
    save_path = os.path.join(save_dir, lang, "item.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    download_file(url, save_path)

# Download achievement.json for each language
for lang in languages:
    url = f"{base_url}{lang}/achievement/achievement.json"
    save_path = os.path.join(save_dir, lang, "achievement/achievement.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    download_file(url, save_path)

# Download gcg/keyword.json,card.json,skill.json for each language
for lang in languages:
    url = [f"{base_url_v2}{lang}/gcg/skill.json", f"{base_url_v2}{lang}/gcg/card.json", f"{base_url_v2}{lang}/gcg/keyword.json"]
    save_path = [os.path.join(save_dir_v2, lang, "gcg", "skill.json"), os.path.join(save_dir_v2, lang, "gcg", "card.json"), os.path.join(save_dir_v2, lang, "gcg", "keyword.json")]
    for i in range(len(url)):
        os.makedirs(os.path.dirname(save_path[i]), exist_ok=True)
        download_file(url[i], save_path[i])

# Helper function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Download localized files for each language
def download_localized_files(category, ids, v = 1):
    for lang in languages:
        for id_ in ids:
            if v == 1:
                localized_url = f"{base_url}{lang}/{category}/{id_}.json"
                localized_save_path = os.path.join(save_dir, lang, category, f"{id_}.json")
            else:
                localized_url = f"{base_url_v2}{lang}/{category}/{id_}.json"
                localized_save_path = os.path.join(save_dir_v2, lang, category, f"{id_}.json")
            os.makedirs(os.path.dirname(localized_save_path), exist_ok=True)
            download_file(localized_url, localized_save_path)

# Load the main JSON files
character_data = load_json(os.path.join(save_dir, "character.json"))
weapon_data = load_json(os.path.join(save_dir, "weapon.json"))
artifact_data = load_json(os.path.join(save_dir, "artifact.json"))
monster_data = load_json(os.path.join(save_dir, "monster.json"))
gcg_data = load_json(os.path.join(save_dir_v2, "gcg.json"))
tower_data = load_json(os.path.join(save_dir, "tower.json"))
rolecombat_data = load_json(os.path.join(save_dir, "rolecombat.json"))
furniture_data_v2 = load_json(os.path.join(save_dir_v2, "furniture.json"))
suite_data_v2 = load_json(os.path.join(save_dir_v2, "suite.json"))

# Load item.json for each language
item_data = {}
for lang in languages:
    item_data[lang] = load_json(os.path.join(save_dir, lang, "item.json"))

# Extract IDs for each category
character_ids = character_data.keys()
weapon_ids = weapon_data.keys()
artifact_ids = artifact_data.keys()
monster_ids = monster_data.keys()
gcg_ids = []
for key, value in gcg_data.items():
    gcg_ids.append(key)
    if 'relate' in value:
        gcg_ids.append(str(value['relate']))
tower_ids = tower_data['version']
rolecombat_ids = rolecombat_data.keys()
furniture_ids = furniture_data_v2.keys()
suite_ids = suite_data_v2.keys()

# Extract item IDs for each language
item_ids = {lang: item_data[lang].keys() for lang in languages}

# Download files for each category and language
download_localized_files("character", character_ids)
download_localized_files("weapon", weapon_ids)
download_localized_files("artifact", artifact_ids)
download_localized_files("monster", monster_ids)
download_localized_files("tower", tower_ids)
download_localized_files("rolecombat", rolecombat_ids)
download_localized_files("gcg", gcg_ids, 2)
download_localized_files("furniture", furniture_ids, 2)
download_localized_files("suite", suite_ids, 2)

# Download localized item files
for lang in languages:
    for id_ in item_ids[lang]:
        localized_item_url = f"{base_url}{lang}/item/{id_}.json"
        localized_item_save_path = os.path.join(save_dir, lang, "item", f"{id_}.json")
        os.makedirs(os.path.dirname(localized_item_save_path), exist_ok=True)
        download_file(localized_item_url, localized_item_save_path)
