from flask import Blueprint
from flask import render_template

from app.models import db_model

preview = Blueprint("preview", __name__)


@preview.route("/<project_ns>")
def preview_main(project_ns: str):
    project_data = db_model.MapProject.query.filter_by(namespace=project_ns).first()
    return render_template("previewer.html", project=project_data)
