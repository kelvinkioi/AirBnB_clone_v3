#!/usr/bin/python3
"""
start your API!
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def app_teardown(exception):
    """
    calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def not_found404(error):
    """
    handler for 404 errors that returns a
    JSON-formatted 404 status code response
    """

    err = {
        "error": "Not Found"
    }
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port)
