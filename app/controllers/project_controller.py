from flask import Blueprint
from flask import render_template, redirect, url_for, abort
from flask import flash
from flask import request

from app.models import db_model, project_operation, tilemap, tilemap_upload

project = Blueprint("project", __name__)


@project.route("/new")
def project_new():
    return render_template("project/project_edit.html", is_new=True)


@project.route("/new", methods=["POST"])
def project_new_save():
    try:
        project_operation.create_new(request.form)
        flash(f"Project {request.form['title']} ({request.form['namespace']}) created!", category="success")
        return redirect(url_for(".project_detail", project_ns=request.form["namespace"]))
    except project_operation.ProjectExist:
        flash(f"Project with namespace {request.form['namespace']} already exist!", category="error")
    except project_operation.InvalidNamespace:
        flash(f"Namespace invalid!", category="error")

    return render_template("project/project_edit.html", project=request.form, is_new=True)


@project.route("/detail/<project_ns>")
def project_detail(project_ns: str):
    try:
        p = project_operation.get_data(project_ns)
        return render_template("project/project_detail.html", project=project_operation.get_data(project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)


@project.route("/edit/<project_ns>")
def project_edit(project_ns: str):
    try:
        return render_template("project/project_edit.html", project=project_operation.get_data(project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)


@project.route("/edit/<project_ns>", methods=["POST"])
def project_edit_save(project_ns: str):
    project_data = db_model.MapProject.query.filter_by(namespace=project_ns).first()
    old_data = {'title': project_data.title, 'namespace': project_data.namespace}
    try:
        project_operation.edit(project_ns, request.form)
        flash(f"Project updated!", category="success")
        if request.form["namespace"] != old_data["namespace"]:
            flash(
                f"Project namespace changed! Update your projects to match the new namespace! "
                f"({old_data['namespace']} -> {request.form['namespace']})",
                category="warning")
        return redirect(url_for(".project_detail", project_ns=request.form["namespace"]))
    except project_operation.ProjectExist:
        flash(f"Project with namespace {request.form['namespace']} already exist!", category="error")
    except project_operation.InvalidNamespace:
        flash(f"Namespace invalid!", category="error")

    return render_template("project/project_edit.html", old_data=old_data, project=request.form)


@project.route("/delete/<project_ns>")
def project_delete(project_ns: str):
    try:
        return render_template("project/project_delete.html", project=project_operation.get_data(project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)


@project.route("/delete/<project_ns>", methods=["POST"])
def project_delete_do(project_ns: str):
    if request.form["namespace"] == project_ns:
        try:
            project_data = project_operation.get_data(project_ns)
            title = project_data.title
            namespace = project_data.namespace
            try:
                tilemap.delete_tiles(project_ns)
                project_operation.delete(project_ns)
                flash(f"Project {title} ({namespace}) deleted!", category="warning")
                return redirect(url_for("dashboard.dashboard_main"))
            except Exception as e:
                flash(f"Project {title} ({namespace}) deletion failed! ({e})", category="error")
        except project_operation.ProjectNotExist:
            flash("Cannot delete project! (namespace {namespace} does not exist)", category="error")
    else:
        flash("Confirmation on project deletion failed!", category="error")

    return redirect(url_for(".project_detail", project_ns=project_ns))


@project.route("/upload/<project_ns>")
def project_upload(project_ns: str):
    try:
        return render_template("project/project_upload.html", project=project_operation.get_data(project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)


@project.route("/upload/<project_ns>", methods=["POST"])
def project_upload_post(project_ns: str):
    # TODO: Resolving file conflicts
    try:
        pattern = request.form['pattern']
        uploaded_file = request.files["archive_file"]
        tilemap_upload.process_zip(project_ns, uploaded_file.stream, pattern)
        flash(f"Tiles uploaded!", category="success")
        return redirect(url_for(".project_detail", project_ns=project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)


@project.route("/download/<project_ns>")
def project_download(project_ns: str):
    try:
        return render_template("project/project_download.html", project=project_operation.get_data(project_ns))
    except project_operation.ProjectNotExist:
        return abort(404)
