import os
import csv

from atimetabler.constants import UnitAssesments, CSV_FIELD_NAMES

CACHE_FOLDER_NAME = "cache"
CACHE_FILE_EXTENSION = "csv"
CACHE_FILE_DELIMITER = ','

def _get_cache_path(unit_code: str) -> str:
    cache_file_name = f"{unit_code.lower()}.{CACHE_FILE_EXTENSION}"
    return os.path.join(CACHE_FOLDER_NAME, cache_file_name)

def _create_cache(cache_path: str):
    with open(cache_path, "w+") as cache_file:
        writer = csv.writer(cache_file)
        writer.writerow(CSV_FIELD_NAMES)

def cache_exists(unit_code: str) -> bool:
    cache_path = _get_cache_path(unit_code)
    return os.path.exists(cache_path)

def write_to_cache(cache_path: str, unit_assesments: UnitAssesments):
    if not os.path.exists(cache_path):
        _create_cache(cache_path)

    with open(cache_path, "a") as cache_file:
        writer = csv.DictWriter(cache_file, CSV_FIELD_NAMES)
        for unit_assesment in unit_assesments:
            writer.writerow(unit_assesment)

def read_from_cache(unit_code: str) -> UnitAssesments:
    unit_assesments = []
    cache_path = _get_cache_path(unit_code)
    with open(cache_path) as cache_file:
        reader = csv.DictReader(cache_file)
        for row in reader:
            unit_assesments.append(row)
    
    return unit_assesments

def cache_unit_assesments(unit_code: str, unit_assesments: UnitAssesments):
    if not os.path.exists(CACHE_FOLDER_NAME):
        os.mkdir(CACHE_FOLDER_NAME)

    cache_path = _get_cache_path(unit_code)
    write_to_cache(cache_path, unit_assesments)