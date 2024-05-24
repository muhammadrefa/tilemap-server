from flask import Blueprint
from flask import abort, request, send_file

from app.models.tilemap import get_tile_filepath, DownloadError

tile = Blueprint("tile", __name__)


@tile.route("/<project>")
def tile_project_home(project: str):
    return abort(403)


@tile.route("/<project>/<int:z>/<int:x>/<int:y>.png", methods=["GET"])
def load_tile(project: str, z: int, x: int, y: int):
    offline_only = False
    if request.args.get("offline"):
        offline_only = True
    try:
        filepath = get_tile_filepath(project, z, x, y,
                                     user_agent=request.headers.get("user-agent"),
                                     offline_only=offline_only)
        return send_file(filepath)
    except FileNotFoundError:
        return abort(404)
    except DownloadError as e:
        return abort(e.status_code)
