from app import app

from app.controllers.dashboard_controller import dashboard
from app.controllers.tile_controller import tile
from app.controllers.project_controller import project
from app.controllers.preview_controller import preview

app.register_blueprint(dashboard)
app.register_blueprint(tile, url_prefix="/tile")
app.register_blueprint(project, url_prefix="/project")
app.register_blueprint(preview, url_prefix="/preview")
