from flask import Blueprint
from flask import render_template, redirect, url_for, abort
from flask import flash
from flask import request

from app import app
from app.models import db_model, app_config

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def dashboard_main():
    project_list = db_model.MapProject.query.with_entities(db_model.MapProject.namespace, db_model.MapProject.title)
    return render_template("dashboard/main.html", projects=project_list.all())


@dashboard.route("/appconfig")
def dashboard_appconfig():
    cfg = app_config.get_configs()
    return render_template("dashboard/appconfig.html", appconfig=cfg, appdata_path=app.config["APPDATA_PATH"])


@dashboard.route("/appconfig", methods=["POST"])
def dashboard_appconfig_save():
    app_config.save_configs(request.form)
    flash(f"App configuration saved!", category="success")
    return redirect(url_for(".dashboard_appconfig"))
