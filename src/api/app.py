from flask import Flask, jsonify, request, make_response, abort, Blueprint
import logging
from random_mob import load as random_mob_load

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_app():
    # init random_mob sub
    random_mob_load()

    # init flask app
    flask_app = Flask(__name__)
    flask_app.debug = True

    # register mob blueprint
    from random_mob import app as random_mob_app
    flask_app.register_blueprint(random_mob_app)

    return flask_app


if __name__ == '__main__':
    create_app().run()
