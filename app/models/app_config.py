from typing import List, Dict

from app import app, db
from app.models import db_model


def get_configs() -> dict:
    app_cfg = dict()
    configs = db_model.AppConfig.query.all()
    for cfg in configs:
        app_cfg[cfg.key] = cfg.value
    return app_cfg


def save_configs(configs: Dict[str, str]):
    for cfg_key in configs:
        cfg = db_model.AppConfig.query.filter_by(key=cfg_key).first()
        is_new = cfg is None
        if is_new:
            cfg = db_model.AppConfig()
            cfg.key = cfg_key
        cfg.value = configs[cfg_key]
        if is_new:
            db.session.add(cfg)
    db.session.commit()


def tile_filepath() -> str:
    cfg_filepath = db_model.AppConfig.query.filter_by(key="tile_filepath").first()
    if cfg_filepath is None:
        cfg_filepath = db_model.AppConfig()
        cfg_filepath.key = "tile_filepath"
        cfg_filepath.value = app.config["APPDATA_PATH"] + "/tiles/{project}/{z}/{x}/{y}.png"
        db.session.add(cfg_filepath)
        db.session.commit()
    elif not cfg_filepath.value:
        cfg_filepath.value = app.config["APPDATA_PATH"] + "/tiles/{project}/{z}/{x}/{y}.png"
        db.session.commit()
    return cfg_filepath.value
