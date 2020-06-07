import os 
from flask import Flask

app = Flask(__name__, instance_relative_config=True)
def create_app(test_config=None):
    
    app.config.from_mapping(
            SECRET_KEY = 'yolo',
            DATABASE = os.path.join(app.instance_path, 'police.sqlite'),
        )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import simdb
    simdb.init_app(app)

    from . import main
    app.register_blueprint(main.bp)

    return app

