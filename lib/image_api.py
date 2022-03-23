from sys import prefix
from flask import Flask, Blueprint, send_file, request, Response
from .visualize import visualize
import io

image_api = Blueprint("image_api", __name__, url_prefix = "/images")

@image_api.route("/types_of_runs", methods=["POST", "GET"])
def generateTypesOfRunResponse():
    """
    This route fetches the run type distribution figure

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotTypesOfRuns(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/run_start_distribution", methods=["POST", "GET"])
def generateStartTimeDistributionResponse():
    """
    This route fetches the run start time distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotRunStartTimeDistribution(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/run_township_distribution", methods=["POST", "GET"])
def generateTownshipDistributionResponse():
    """
    This route fetches the run township distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotRunTownships(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/apparatus_distribution", methods=["POST", "GET"])
def generateApparatusDistributionResponse():
    """
    This route fetches the run apparatus distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotApparatusUsageFrequency(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/given_aid", methods=["POST", "GET"])
def generateGivenAidDistributionResponse():
    """
    This route fetches the given aid distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotGivenAid(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/taken_aid", methods=["POST", "GET"])
def generateTakenAidDistributionResponse():
    """
    This route fetches the taken aid distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotTakenAid(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200


@image_api.route("/shift_coverage", methods=["POST", "GET"])
def generateShiftCoverageDistributionResponse():
    """
    This route fetches the shift coverage distribution figures.

    returns..
        The figure and status 200
    """
    requestValues = request.json
    startDate = requestValues["startDate"]
    endDate = requestValues["endDate"]
    figure = visualize.plotShiftCoverage(startDate, endDate)
    
    if figure == None:
        return "No incidents during provided period", 500
    return send_file(io.BytesIO(figure.getbuffer()), mimetype = "impge/png"), 200