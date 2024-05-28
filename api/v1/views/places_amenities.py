#!/usr/bin/python3
"""State objects that handle all default RESTful API actions"""
import os
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.place import Place
from flask import abort, request, jsonify

db_mode = os.getenv("HBNB_TYPE_STORAGE")

@app_views.route("/places/<place_id>/amenities", strict_slashes=False, methods=["GET"])
def place_amenities(place_id):
    """Retrieve place amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)  # Changed to 404 for resource not found
    amenities_list = []
    if db_mode == "db":
        amenities = place.amenities
        amenities_list = [amenity.to_dict() for amenity in amenities]
    else:
        amenities_list = place.amenity_ids
    return jsonify(amenities_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"])
def delete_amenity(place_id, amenity_id):
    """Delete an amenity by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        place_amenities = place.amenities
        if amenity in place_amenities:
            place_amenities.remove(amenity)
            storage.save()
        else:
            abort(404)
    else:
        if amenity_id in place.amenity_ids:
            place.amenity_ids.remove(amenity_id)
            storage.save()
        else:
            abort(404)
    return jsonify({}), 200  # Corrected the response structure


@app_views.route("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=["POST"])
def link_amenity(place_id, amenity_id):
    """Link Amenity to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if db_mode == "db":
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
        else:
            return jsonify(amenity.to_dict()), 200
    else:
        if amenity_id not in place.amenity_ids:
            place.amenity_ids.append(amenity_id)
            storage.save()
        else:
            return jsonify(amenity.to_dict()), 200
    return jsonify(amenity.to_dict()), 201  # Corrected the response structure and status code
