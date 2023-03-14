from my_apps import app
from werkzeug.utils import import_string

# configuration using objects
cfg = import_string('config.BaseConfig')()
app.config.from_object(cfg)
