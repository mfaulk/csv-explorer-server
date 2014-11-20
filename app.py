"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import requests
import json
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from flask.ext.cors import CORS
from bson import json_util
from bson.objectid import ObjectId
from mongoengine import connect
from models import Table, Row, Cell

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.debug=True
#app.logger.debug('=== A debug message ===')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
cors = CORS(app, resources={r'/*' : {"origins":"*"}})

MONGO_DATABASE_NAME = 'memex'
connect(MONGO_DATABASE_NAME)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def insert_test_table():
    file_name = "the_file_name.csv"
    table = Table(file_name).save()

    file_contents = """ headerA,headerB,headerC,headerD
                    aaa,bbb,cc,ddddd
                    1,2,44,10"""
    for line in file_contents.split('\n'):
        cols = line.split(',')
        r = Row()
        r.populate(cols)
        app.logger.debug(type(r))
        table.rows.append(r)
    table.save()

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/v1/tables', methods=['GET'])
def tables():
    """ Return a list of Tables
    Example: /api/vi/tables/?limit=10&offset=20
    :return:
    """
    if request.method == 'GET':
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        results = Table.objects[offset:offset+limit]
        app.logger.debug(type(results))
        return results.to_json()

 # @app.route('/upload/', methods=['GET', 'POST'])
 # def upload():
 #     if request.method == 'POST':
 #         file = request.files['file']
 #         if file:
 #             filename = secure_filename(file.filename)
 #             print filename
 #             contents = file.read()
 #             t = Table(filename=filename)
 #             for line in contents.split('\n'):
 #                 cols = line.split(',')
 #                 app.logger.debug(cols)
 #                 r = Row().populate(cols)
 #                 t.rows.append(r)

#             #TODO Remove hard-coded URL. What is the equivalent of url_for for flask-restless APIs?
#             data_url = 'http://127.0.0.1:5000/api/v1/tables/' + str(t.id)
#             app.logger.debug("requesting " + data_url)
#             # rv is of type requests.models.response
#             rv = requests.get(data_url)
#             # app.logger.debug(type(rv))
#             app.logger.debug(rv.content)
#             app.logger.debug(rv.status_code)
#             app.logger.debug("...done.")
#
#             # CORS seems to make these unnecessary:
#             # resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin','*')
#             # resp.headers['Access-Control-Allow-Credentials'] = 'true'
#             # resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
#             # resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers', 'Authorization' )
#             # resp.headers['Access-Control-Max-Age'] = '1'
#             app.logger.debug("Returning.")
#             return rv.content

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
