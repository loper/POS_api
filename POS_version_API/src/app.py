from os.path import join
from os import environ

from flask import Flask, jsonify, send_from_directory

import utils
from config import TEMPLATES_DIR, APP_AUTHOR, APP_VERSION
from config import LIMITS

APP = Flask(__name__)


@APP.route("/")
def show_details():
    return "<html>" + \
           "<head><title>GK POS API</title></head>" + \
           "<body>" + \
           "<h1>POS Version API v{}</h1>".format(APP_VERSION) + \
        "<span>by {}</span>".format(APP_AUTHOR) + \
        "</body>" + \
        "</html>"


@APP.route('/latest')
def get_latest_version():
    if 'TEMPLATES_DIR' in environ:
        templates_dir = environ['TEMPLATES_DIR']
    else:
        templates_dir = TEMPLATES_DIR
    ver_latest, ver_parent = utils.find_latest_pos(templates_dir, LIMITS)
    return jsonify({'parent': ver_parent, 'version': ver_latest})


@APP.route('/versions')
def get_all_versions():
    if 'TEMPLATES_DIR' in environ:
        templates_dir = environ['TEMPLATES_DIR']
    else:
        templates_dir = TEMPLATES_DIR
    versions = utils.find_latest_pos(templates_dir, LIMITS, dry_run=True)
    status = bool(versions)
    return jsonify({'status': status, 'versions': versions})


@APP.route('/experimental/latest')
def get_latest_version2():
    if 'TEMPLATES_DIR' in environ:
        templates_dir = environ['TEMPLATES_DIR']
    else:
        templates_dir = TEMPLATES_DIR
    ver_latest, ver_parent = utils.experimental_find_latest_pos(templates_dir)
    return jsonify({'parent': ver_parent, 'version': ver_latest})


@APP.route('/favicon.ico')
def favicon():
    return send_from_directory(join(APP.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    APP.run(debug=False, host='0.0.0.0')
