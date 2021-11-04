from flask import Flask, jsonify, request
from datetime import datetime
import json
from .generate_report import generate_report as grp
from .payroll import payroll
import sqlite.check_database as cdb
from flask.wrappers import Request

app = Flask(__name__)

"""
This method will run before the first request to the server. It ensures that the DB exists and is ready for use.
"""
@app.before_first_request
def ensure_database_is_ready():
    cdb.check_database.check()

"""
This section will return an error message to the requester (the UI for us)
if an invalid address is sent a request.
"""
@app.errorhandler(404)
def invalid_route():
    return(jsonify({"errorCode": 404, "message": "Route not found! Requested address was: " + Request.full_path}))


"""
This function is for the UI to determine if the server is running. If the server
sees any call to this address, it will return a signal signifying the sercer is alive.
If the UI recieves a socket error, that means the server is not running and needs
to be started.

inputs..
    (request) Any request on this address
returns.. 
    case 1: A Json object signifying the server is alive
"""
@app.route('/verify', methods=["GET", "POST"])
def verify_awake():
    return jsonify({"result": True})


"""
This is the function responsible for accepting a request from the UI that
contains a list of file paths and forwarding that to the backend to insert
the information into the database.

inputs..
    (request): A post request containing a Json array of strings
returns..
    case 1: A Json array containing true (in the case of sucessful inserts)
    case 2: A list of files that failed to be insterted
"""
@app.route('/submit_reports', methods=["GET", "POST"])
def submit_reports():
    files = request.json

    results = payroll.loadWorkBooks(files)

    return jsonify(results)

"""
This is the function responsible for accepting a request from the UI
to tell the backend the user wishes to generate the pay reports.

inputs..
    (request): A Json object containing two key value pairs
        startDate and endDate that express the start and end of the
        pay period as strings
returns.. 
    case 1: A Json array that either contains a True value
        and several strings
    case 2: A Json array that contains one or more strings in
        the event that the files could not be generated
"""
@app.route('/generate_report', methods=["GET", "POST"])
def generate_reports():
    dates = request.json
    startDate = dates["startDate"].split(" ")[0]
    endDate = dates["endDate"].split(" ")[0]

    results = grp.generate_report(startDate, endDate)

    return jsonify(results)
