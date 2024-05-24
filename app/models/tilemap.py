import os
import random
import requests
import shutil

from pathlib import Path

from app import app
from app.models import app_config, project_operation


class DownloadError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def get_tile_filepath(project: str, z: int, x: int, y: int, user_agent: str = None,
                      offline_only: bool = True) -> str:
    # Get tile source URL and limitation
    try:
        tile_sources, zoom_limit, map_opts = project_operation.get_tile_source(project)
    except project_operation.ProjectNotExist:
        raise FileNotFoundError

    if (zoom_limit[0] is not None) and (z < zoom_limit[0]):
        raise FileNotFoundError
    if (zoom_limit[1] is not None) and (zoom_limit[1] < z):
        raise FileNotFoundError

    tile_filepath = app_config.tile_filepath()
    tile_filepath = tile_filepath.format_map({'project': project, 'z': z, 'x': x, 'y': y})

    if not os.path.isabs(tile_filepath):
        tile_filepath = f"{app.config['APPDATA_PATH']}/{tile_filepath}"

    if not os.path.exists(f"{tile_filepath}") and not offline_only:
        if tile_sources is None:
            raise DownloadError("Tile source URL not set!", 404)

        tile_source_list = tile_sources.split()
        download_success = False

        while len(tile_source_list) and not download_success:
            _source_idx = 0
            if "urls_in_sequence" not in map_opts:
                _source_idx = random.randrange(0, len(tile_source_list))
            tile_source = tile_source_list.pop(_source_idx)
            url_pic = tile_source.format_map({'z': z, 'x': x, 'y': y})
            # print(f"Download tile from {url_pic}")

            if user_agent is None:
                r_pic = requests.get(url_pic)
            else:
                r_pic = requests.get(url_pic, headers={"user-agent": user_agent})
            print(f"Download tile from {url_pic} status {r_pic.status_code}")

            if r_pic.status_code == 200:
                tile = bytearray()
                for chunk in r_pic.iter_content(chunk_size=128):
                    tile += chunk
                store_tile(bytes(tile), project, z, x, y)
                download_success = True
            elif len(tile_source_list) == 0:
                raise DownloadError(f"Returned {r_pic.status_code}", r_pic.status_code)

    if os.path.exists(f"{tile_filepath}"):
        return f"{tile_filepath}"
    else:
        raise FileNotFoundError


def delete_tiles(project: str):
    tile_filepath = app_config.tile_filepath()
    tile_filepath = tile_filepath.format_map({'project': project, 'z': "", 'x': "", 'y': "0"})

    if not os.path.isabs(tile_filepath):
        tile_filepath = f"{app.config['APPDATA_PATH']}/{tile_filepath}"
    tile_directory = str(Path(tile_filepath).with_suffix(""))[:-1]
    shutil.rmtree(tile_directory)


def store_tile(tile: bytes, project: str, z: int, x: int, y: int):
    tile_filepath = app_config.tile_filepath()
    tile_filepath = tile_filepath.format_map({'project': project, 'z': z, 'x': x, 'y': y})

    try:
        os.umask(0)
        os.makedirs(os.path.dirname(tile_filepath))
    except FileExistsError:
        pass

    with open(f"{tile_filepath}", 'wb') as pic:
        pic.write(tile)
