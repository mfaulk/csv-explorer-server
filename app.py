"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import requests
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from flask.ext.cors import CORS
from bson import json_util
from bson.objectid import ObjectId
from mongoengine import connect
from models import Table, Row, Cell


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
cors = CORS(app, resources={r'/*' : {"origins":"*"}})

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

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

@app.route('/api/v1/table/<table_id>', methods=['GET'])
def table(table_id):
    if request.method == 'GET':
        result = Table.objects.get(id=table_id)
        return result.to_json()


@app.route('/upload/', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            #filename = secure_filename(file.filename)
            file_name = file.filename
            app.logger.debug("Received " + file_name)
            contents = file.read()
            table = Table(file_name=file_name)
            for line in contents.split('\n'):
                cols = line.split(',')
                app.logger.debug(cols)
                r = Row()
                r.populate(cols)
                table.rows.append(r)
            table.save()
            json_val = table.to_json()
            app.logger.debug(json_val)
            return table.to_json()
        else:
            app.logger.debug("No file provided to /upload/")
    else:
        app.logger.debug("Unimplemented /upload/ request method: " + request.method)

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
