from app import db


class AppConfig(db.Model):
    __tablename__ = "app_config"
    __table_args__ = {"extend_existing": True}
    key = db.Column(db.Text, primary_key=True, unique=True, nullable=False)
    value = db.Column(db.Text)


class MapProject(db.Model):
    __tablename__ = "map_project"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    namespace = db.Column(db.Text, unique=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
    tile_source = db.Column(db.Text)
    tile_zoom_min = db.Column(db.Integer)
    tile_zoom_max = db.Column(db.Integer)
    map_opts = db.Column(db.Text)
    previewer_center_lat = db.Column(db.Float)
    previewer_center_lon = db.Column(db.Float)
    previewer_zoom = db.Column(db.Integer)
    previewer_opts = db.Column(db.Text)


def create_tables():
    db.create_all()
