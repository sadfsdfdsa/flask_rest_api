from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate

from config import Config

# main app
app = Flask(__name__)

# main app config
app.config.from_object(Config)

# soft app config
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models and objects imports
from main.Settings import Settings
from main.Api import *


# Auth handling
@auth.get_password
def get_password(username):
    if len(User.query.filter_by(username=username).all()) != 0:
        return User.query.filter_by(username=username).first().password
    return None


# Errors handling

def base_error_handler(code):
    return make_response(jsonify(response={'error': Settings.errors_by_code[code], 'code': code}), code)


@auth.error_handler
def unauthorized():
    return base_error_handler(401)


@app.errorhandler(404)
def not_found(error):
    return base_error_handler(404)


# Routing

@app.route('/api/<string:version>/<string:method>/', methods=['GET'])
# @auth.login_required
def get_objects(version, method):
    if version in Apis_version_dict:
        if method in Apis_version_dict[version].api_objects:
            return jsonify(response=[i.serialize for i in Apis_version_dict[version].api_objects[method].query.all()])
    return base_error_handler(404)


@app.route('/api/<string:version>/<string:method>/<int:id>', methods=['GET'])
# @auth.login_required
def get_object_by_id(version, method, id):
    if version in Apis_version_dict:
        if method in Apis_version_dict[version].api_objects:
            return jsonify(response=[i.serialize for i in
                                     Apis_version_dict[version].api_objects[method].query.filter_by(id=id).all()])
    return base_error_handler(404)


@app.route('/api/<string:version>/<string:method>/', methods=['POST'])
@auth.login_required
def create_object(version, method):
    if not request.json:
        return base_error_handler(404)
    if version in Apis_version_dict:
        if method in Apis_version_dict[version].api_objects:
            try:
                return jsonify(response=Apis_version_dict[version].post_object(method, db, **request.json).serialize)
            except exc.IntegrityError:
                return base_error_handler(400)
    return base_error_handler(404)


@app.route('/api/<string:version>/<string:method>/<int:id>', methods=['PUT'])
@auth.login_required
def update_object(version, method, id):
    if not request.json:
        return base_error_handler(404)
    if version in Apis_version_dict:
        if method in Apis_version_dict[version].api_objects:
            try:
                object = Apis_version_dict[version].put_object_by_id(method, db, id, **request.json)
                if object == None:
                    return base_error_handler(400)
                return jsonify(response=object)
            except exc.IntegrityError:
                return base_error_handler(400)
    return base_error_handler(404)


@app.route('/api/<string:version>/<string:method>/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(version, method, id):
    if version in Apis_version_dict:
        if method in Apis_version_dict[version].api_objects:
            if Apis_version_dict[version].delete_object_by_id(method, db, id):
                return jsonify(response="success")
            else:
                return base_error_handler(400)
    return base_error_handler(404)


"""
heroku login
git clone git://github.com/miguelgrinberg/microblog.git
heroku create flask-microblog
heroku addons:add heroku-postgresql:dev
heroku config:set HEROKU=1
pip freeze > requirements.txt
git push heroku master
heroku run init
heroku run upgrade
heroku logs
git commit -a -m "your message goes here"
"""

if __name__ == '__main__':
    app.run()
