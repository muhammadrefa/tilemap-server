import re
from typing import Tuple

from app import db
from app.models import db_model


class ProjectNotExist(Exception):
    pass


class ProjectExist(Exception):
    pass


class InvalidNamespace(Exception):
    pass


def create_new(project_data: dict):
    # Check if namespace already exist
    if db_model.MapProject.query.filter_by(namespace=project_data["namespace"]).count() > 0:
        raise ProjectExist

    # Check for invalid characters in namespace
    if re.search("[^A-za-z0-9-_]", project_data["namespace"]) is not None:
        raise InvalidNamespace

    new_project = db_model.MapProject()
    new_project.namespace = project_data["namespace"]
    new_project.title = project_data["title"]
    if len(project_data["tile_source"]):
        new_project.tile_source = project_data["tile_source"]
    if len(project_data["tile_zoom_min"]):
        new_project.tile_zoom_min = project_data["tile_zoom_min"]
    if len(project_data["tile_zoom_max"]):
        new_project.tile_zoom_max = project_data["tile_zoom_max"]
    if len(project_data["previewer_center_lat"]):
        new_project.previewer_center_lat = project_data["previewer_center_lat"]
    if len(project_data["previewer_center_lon"]):
        new_project.previewer_center_lon = project_data["previewer_center_lon"]
    if len(project_data["previewer_zoom"]):
        new_project.previewer_zoom = project_data["previewer_zoom"]

    db.session.add(new_project)
    db.session.commit()


def edit(old_project_name: str, project_data: dict):
    # Check if namespace changed and new namespace already exist
    if project_data["namespace"] != old_project_name \
            and db_model.MapProject.query.filter_by(namespace=project_data["namespace"]).count() > 0:
        raise ProjectExist

    # Check for invalid characters in new namespace
    if re.search("[^A-za-z0-9-_]", project_data["namespace"]) is not None:
        raise InvalidNamespace

    project = db_model.MapProject.query.filter_by(namespace=old_project_name).first()
    project.namespace = project_data["namespace"]
    project.title = project_data["title"]
    if len(project_data["tile_source"]):
        project.tile_source = project_data["tile_source"]
    if len(project_data["tile_zoom_min"]):
        project.tile_zoom_min = project_data["tile_zoom_min"]
    if len(project_data["tile_zoom_max"]):
        project.tile_zoom_max = project_data["tile_zoom_max"]
    if len(project_data["previewer_center_lat"]):
        project.previewer_center_lat = project_data["previewer_center_lat"]
    if len(project_data["previewer_center_lon"]):
        project.previewer_center_lon = project_data["previewer_center_lon"]
    if len(project_data["previewer_zoom"]):
        project.previewer_zoom = project_data["previewer_zoom"]

    db.session.commit()


def delete(project_namespace: str):
    project = db_model.MapProject.query.filter_by(namespace=project_namespace).first()
    if project is None:
        raise ProjectNotExist
    db.session.delete(project)
    db.session.commit()


def get_data(project_namespace: str) -> db_model.MapProject:
    project = db_model.MapProject.query.filter_by(namespace=project_namespace).first()
    if project is None:
        raise ProjectNotExist
    return project


def get_tile_source(project_namespace: str) -> Tuple[str, Tuple[int, int], dict]:
    project = db_model.MapProject.query.filter_by(namespace=project_namespace).first()
    if project is None:
        raise ProjectNotExist

    map_opts = dict()
    try:
        for opt in project.map_opts.split():
            _opt = opt.split("=")
            try:
                map_opts[_opt[0]] = _opt[1]
            except IndexError:
                map_opts[_opt[0]] = ""
    except AttributeError:
        pass

    return project.tile_source, (project.tile_zoom_min, project.tile_zoom_max), map_opts
