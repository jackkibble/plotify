import os
import sqlite3
import json
from functools import wraps

from flask import Flask, Response, g, send_file, send_from_directory, request

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'plotify.db')
PORT = 8080

webapp = Flask(__name__)


def get_db() -> sqlite3.Connection:
    """
    Fetches a request-scoped database connection
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("file:{}?mode=ro".format(DATABASE_PATH), uri=True)
    return db


@webapp.teardown_appcontext
def close_connection(exception):
    """
    Close database at the end of each request if required
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def json_response(f):
    @wraps(f)
    def inner(*args, **kwargs):
        result = f(*args, **kwargs)
        return Response(json.dumps(result), mimetype="application/json")
    return inner


@webapp.route("/")
def index():
    return send_file("static/index.html")


@webapp.route("/dist/<path:path>")
def static_dist(path):
    return send_from_directory("static/dist", path)


@webapp.route("/api/attributes")
@json_response
def get_attributes():
    """
    Should fetch a list of unique student attributes

    Response format:
    {
        attributes: [
            {
                name: "...",
            },
            ...
        ]
    }
    """
    # TODO Implement
    pass


@webapp.route("/api/chart", methods=["POST"])
@json_response
def get_chart():
    """
    Should fetch the data for the chart
    The request may have POST data

    Response format:
    {
        chartType: ChartType,
        data: [Data],
        options: Options,
    }
    where ChartType, Data, and Options are as demonstrated on https://react-google-charts.com/
    """
    # TODO implement this
    pass