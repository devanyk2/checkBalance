import os 
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
    
app.config.from_mapping(
        SECRET_KEY = 'yolo',
            DATABASE = os.path.join(app.instance_path, 'police.sqlite'),
        )

#app.config.from_pyfile('config.py', silent=True)
 

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import simdb

from . import main
app.register_blueprint(main.bp)


