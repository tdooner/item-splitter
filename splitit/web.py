import os
import sys
import ConfigParser

from flask import Flask
from flask import g
from flask import redirect
from flask import session
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from models.shared import db


sys.path.append(os.getcwd())
base = os.path.abspath(os.path.dirname(__file__))

def make_app(environment = 'production'):
    app = Flask(__name__)
    load_config(app, environment)
    register_blueprints(app)
    db.init_app(app)
    return app

def register_blueprints(app):
    import views_setup, views_auction
    app.register_blueprint(views_setup.setup_views)
    app.register_blueprint(views_auction.auction_views)

def load_config(app, environment):
    config = ConfigParser.ConfigParser({
        'base_path' : base,
    })
    config.optionxform = str   # case-sensitive keys
    config.read(os.path.join(base, 'config/%s.conf' % environment))
    app.config.update(dict(config.items('SplitIt')))

def run_webserver(app):
    app.debug = True
    app.run()

splitit_app = make_app()

if __name__ == '__main__':
    run_webserver(splitit_app)
