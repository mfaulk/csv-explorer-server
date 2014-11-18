"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import requests
from flask import Flask, render_template, request, redirect, url_for, Response, make_response
from werkzeug import secure_filename
from flask.ext.cors import CORS
import flask.ext.restless
from pandas import DataFrame, read_csv
import pandas as pd
from database import db_session
from models import *

UPLOAD_FOLDER = '/Users/mfaulk/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.debug=True
app.logger.debug('=== A debug message ===')
#app.logger.warn('=== A warn message ===')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

cors = CORS(app, resources={r'/*' : {"origins":"*"}})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Create the Flask-Restless API manager
manager = flask.ext.restless.APIManager(app, session=db_session)
API_PREFIX="/api/v1"

manager.create_api(Table, url_prefix=API_PREFIX, methods=['GET', 'POST', 'DELETE'])

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            print filename
            rawcontents = file.read()
            t = Table(filename, rawcontents)
            db_session.add(t)
            db_session.commit()
            print(t.id)

            #df = pd.read_csv(file, header=None, sep='\t', error_bad_lines=False)
            #print(df.shape)
            #print(df.to_json())

            #TODO Remove hard-coded URL. What is the equivalent of url_for for flask-restless APIs?
            data_url = 'http://127.0.0.1:5000/api/v1/tables/' + str(t.id)
            app.logger.debug("requesting " + data_url)
            # rv is of type requests.models.response
            rv = requests.get(data_url)
            app.logger.debug(type(rv))
            app.logger.debug(rv.content)
            app.logger.debug(rv.status_code)
            app.logger.debug("...done.")

            # CORS seems to make these unnecessary:
            # resp.headers['Access-Control-Allow-Origin'] = flask.request.headers.get('Origin','*')
            # resp.headers['Access-Control-Allow-Credentials'] = 'true'
            # resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
            # resp.headers['Access-Control-Allow-Headers'] = flask.request.headers.get('Access-Control-Request-Headers', 'Authorization' )
            # resp.headers['Access-Control-Max-Age'] = '1'
            app.logger.debug("Returning.")
            return rv.content

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
