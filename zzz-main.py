import os
import requests
import json
import time
import logging

# Base URLs
base_url = "https://api.hakush.in/zzz/data/"
languages = ["zh", "en", "ja", "ko"]

# List of main JSON files to download
main_files = [
    "character.json",
    "weapon.json",
    "equipment.json",
    "bangboo.json"
]

# Directory to save the files
save_dir = "./zzz/data"

# Create the save directory if it doesn't exist
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Set up logging
logger = logging.getLogger()
logger.setLevel('DEBUG')
BASIC_FORMAT = "%(asctime)s >> %(levelname)s - %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()
chlr.setFormatter(formatter)
chlr.setLevel('INFO')
fhlrd = logging.FileHandler("./zzz-app-debug.log", encoding='utf-8')
fhlrd.setFormatter(formatter)
fhlri = logging.FileHandler("./zzz-app-info.log", encoding='utf-8')
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
    time.sleep(0.1)

# Download new.json
download_file('https://api.hakush.in/zzz/new.json', os.path.join(save_dir, "../new.json"))

# Download main JSON files
for file in main_files:
    url = base_url + file
    save_path = os.path.join(save_dir, file)
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

# Helper function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Download localized files for each language
def download_localized_files(category, ids):
    for lang in languages:
        for id_ in ids:
            localized_url = f"{base_url}{lang}/{category}/{id_}.json"
            localized_save_path = os.path.join(save_dir, lang, category, f"{id_}.json")
            os.makedirs(os.path.dirname(localized_save_path), exist_ok=True)
            download_file(localized_url, localized_save_path)

# Load the main JSON files
character_data = load_json(os.path.join(save_dir, "character.json"))
weapon_data = load_json(os.path.join(save_dir, "weapon.json"))
equipment_data = load_json(os.path.join(save_dir, "equipment.json"))
bangboo_data = load_json(os.path.join(save_dir, "bangboo.json"))

# Load item.json for each language
item_data = {}
for lang in languages:
    item_data[lang] = load_json(os.path.join(save_dir, lang, "item.json"))

# Extract IDs for each category
character_ids = character_data.keys()
weapon_ids = weapon_data.keys()
equipment_ids = equipment_data.keys()
bangboo_ids = bangboo_data.keys()

# Extract item IDs for each language
item_ids = {lang: item_data[lang].keys() for lang in languages}

# Download files for each category and language
download_localized_files("character", character_ids)
download_localized_files("weapon", weapon_ids)
download_localized_files("equipment", equipment_ids)
download_localized_files("bangboo", bangboo_ids)

# Download localized item files
for lang in languages:
    for id_ in item_ids[lang]:
        localized_item_url = f"{base_url}{lang}/item/{id_}.json"
        localized_item_save_path = os.path.join(save_dir, lang, "item", f"{id_}.json")
        os.makedirs(os.path.dirname(localized_item_save_path), exist_ok=True)
        download_file(localized_item_url, localized_item_save_path)
