import typing
import zipfile
from .tilemap import store_tile


def get_pattern(pattern_str: str) -> list:
    pattern = list()
    pos_curr = 0
    pos_temp = 0
    find_open = True

    while pos_temp >= 0:
        pos_temp = pattern_str[pos_curr:].find("{" if find_open else "}")
        find_open = not find_open
        if pos_temp >= 0:
            pattern.append(pattern_str[pos_curr:pos_curr + pos_temp])
            pos_curr += pos_temp + 1
        else:
            pattern.append(pattern_str[pos_curr:])

    # print("pattern str :", pattern_str)
    # print("pattern list:", pattern)
    return pattern


def get_value(filename: str, pattern: list) -> dict:
    result = dict()
    pos_curr = 0
    pos_temp = 0

    # Check for first pattern
    if filename.find(pattern[0]) != 0:
        return None
    pos_curr = len(pattern[0])
    for i in range(1, len(pattern), 2):
        pos_temp = filename[pos_curr:].find(pattern[i + 1])
        result[pattern[i]] = filename[pos_curr:pos_curr + pos_temp]
        pos_curr += pos_temp + len(pattern[i + 1])

    pos_curr -= len(pattern[-1])
    # Check for extension
    if pos_curr < len(filename) - 1:
        if filename[pos_curr:] != pattern[-1]:
            return None
    elif len(pattern[-1]):
        return None

    return result


def process_zip(project: str, zip_filestream: typing.IO[bytes], pattern_str: str):
    pattern = get_pattern(pattern_str)
    uploaded = zipfile.ZipFile(zip_filestream)
    for file in uploaded.filelist:
        tile_prop = get_value(file.filename, pattern)
        if tile_prop is None:
            continue

        z = x = y = 0
        if ("z" in tile_prop) and ("x" in tile_prop) and ("y" in tile_prop):
            try:
                z = int(tile_prop["z"])
                x = int(tile_prop["x"])
                y = int(tile_prop["y"])
            except ValueError:
                continue
        tile_data = uploaded.read(file.filename)
        store_tile(tile_data, project, z, x, y)
