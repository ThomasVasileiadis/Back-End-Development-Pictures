from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # Find the picture in 'data' list that matches the given id
    picture = next((item for item in data if item['id'] == id), None)
    # If the picture doesn't exist, return a 404 error
    if picture is None:
        abort(404)
    return jsonify(picture)


######################################################################
# CREATE A PICTURE
######################################################################
@app.route('/picture', methods=['POST'])
def create_picture():
    picture_data = request.get_json()

    # Check if the picture with the same ID already exists
    if any(picture['id'] == picture_data['id'] for picture in data):
        # If a duplicate is found, send a 302 status code back with a capitalized message
        return jsonify({"Message": "picture with id {} already present".format(picture_data['id'])}), 302

    # If no duplicate is found, add the picture to the 'data' list
    data.append(picture_data)
    return jsonify(picture_data), 201  # Changed status code to 201 for created resources



######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture_data = request.json
    existing_picture = next((item for item in data if item['id'] == id), None)

    if existing_picture is not None:
        # Assuming picture_data contains all the fields for the picture
        existing_picture.update(picture_data)
        return jsonify(existing_picture), 200
    else:
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data  # Ensure you are modifying the global data list
    picture = next((item for item in data if item['id'] == id), None)
    
    if picture:
        data.remove(picture)
        return jsonify({}), 204  # No Content
    else:
        return jsonify({"message": "picture not found"}), 404