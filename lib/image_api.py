from flask import Blueprint, jsonify, request, send_file
from visualize import visualize

image_api = Blueprint("image_api", __name__)

@image_api.route("/types_of_runs", methods=["POST"])
def generate_graphics():
    """
    A temporary route to allow easier generating of
    the sample matplotlib files.

    returns..
        True upon completion
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    print("Generating graphics...")
    # PLACE YOU CALL TO THE VISUALIZATION FUNCTIONS HERE
    figure = visualize.plotTypesOfRuns(startDate, endDate)
    print("Graphics generated...")
    
    return send_file(figure), 200