
import os
from flask import Flask, render_template, request, redirect, url_for, Response, make_response, abort
from flask.ext.cors import CORS
import json
from mongoengine import connect
from models import Table, Row, Cell
from factors.factor_graph import FactorGraph
from framework import get_factor_extensions


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')
cors = CORS(app, resources={r'/*' : {"origins":"*"}})

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

MONGO_DATABASE_NAME = 'memex'
connect(MONGO_DATABASE_NAME)

factor_graph = FactorGraph()

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


###
# Factor Graph API
###

# Get graph
@app.route('/api/v1/graph', methods=['GET'])
def graph():
    if request.method == 'GET':
        return factor_graph.to_json()

# Get Factor types
@app.route('/api/v1/factors', methods=['GET'])
def factors():
    if request.method == 'GET':
        factor_list = get_factor_extensions()
        return json.dumps({"factor-types": factor_list})

# Get nodes
@app.route('/api/v1/graph/nodes', methods=['GET', 'POST'])
def nodes():
    if request.method == 'GET':
        return factor_graph.nodes_to_json()
    elif request.method == 'POST':
        if request.headers['content-type'] == 'application/json':
            # Ensure data is valid JSON
            try:
                data = json.loads(request.data)
            except ValueError:
                return Response(status=405)
            node_type = data['node_type']
            node_id = factor_graph.add_node(node_type)
            return json.dumps({"node_id":node_id})
        else:
            # Unsupported content type.
            return Response(status=400)

        # if not request.json or not 'node_type' in request.json:
        #     abort(400)
        # else:
        #     node_type = request.json['node_type']
        #     node_id = factor_graph.addNode(node_type)
        #     return node_id

@app.route('/api/v1/graph/node/<node_id>', methods=['GET', 'DELETE'])
def node(node_id):
    if request.method == 'GET':
        return factor_graph.node_to_json(node_id)
    elif request.method == 'DELETE':
        factor_graph.delete_node(node_id)
        return json.dumps({"node_id": node_id})


@app.route('/api/vi/graph/edges', methods=['GET','POST'])
@app.route('/api/vi/graph/edges/<edge_id>', methods=['GET','DELETE'])
def edges(edge_id=None):
    if edge_id:
        # Individual edge
        if request.method == 'GET':
            edge = factor_graph.get_edge(edge_id)
            return edge.to_json()

        elif request.method == 'DELETE':
            factor_graph.delete_edge_by_id(edge_id)
            return json.dumps({"edge_id": edge_id})
    else:
        # All edges
        if request.method == 'GET':
            edges = factor_graph.get_edges()
            edge_data = [{"id": e.id, "src_uri": e.src_uri, "dest_uri": e.dest_uri} for e in edges]
            return json.dumps({"edges": edge_data})
        elif request.method == 'POST':
            if request.headers['content-type'] == 'application/json':
                try:
                    data = json.loads(request.data)
                    src_uri = data['src_uri']
                    dest_uri = data['dest_uri']
                    edge_id = factor_graph.add_edge(src_uri, dest_uri)
                    if not edge_id:
                        app.logger.debug("No id?")
                    return json.dumps({"edge_id": edge_id})
                except ValueError:
                    return Response(status=405)

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
