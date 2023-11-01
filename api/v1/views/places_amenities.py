#!/usr/bin/python3
"""places_amenities.py"""
from api.v1.views import app_views
import os
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    location = storage.get("Place", place_id)
    if location is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = location.amenities
    else:
        amenity_objects = location.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    location = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if location is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = location.amenities
    else:
        place_amenities = location.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    location.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    location = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if location is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = location.amenities
    else:
        place_amenities = location.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    location.save()
    return make_response(jsonify(amenity.to_dict()), 201)
