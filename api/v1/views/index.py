#!/usr/bin/python3
"""
API index
"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status')
def status():
    """
    json response as the status

    Returns:
        JSON: json object
    """
    status = {
        "status": "OK"
    }
    return jsonify(status)


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    count of databases
    """

    models = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }

    r_dict = {}
    for key, value in models.items():
        r_dict[key] = storage.count(value)
    return jsonify(r_dict)
