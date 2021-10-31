from flask import Flask, jsonify, request
from datetime import datetime
import json
import payroll

from flask.wrappers import Request

app = Flask(__name__)

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

    lst: results = payroll.loadWorkbooks(files)

    """
    Remove this line when the above work is implementd.
    You can test the flutter by changing what is in this list.
    True is the case when it works, a list of strings (specifically)
    File locations for when it fails. Just comment the one you don't
    want then restart the server.
    """
    #results = [True]
    results = ['C:\\Users\\dalto\\Desktop\\509.xlsx', 'C:\\Users\\dalto\\Desktop\\510.xlsx', 'C:\\Users\\dalto\\Desktop\\511.xlsx', 'C:\\Users\\dalto\\Desktop\\512.xlsx', 'C:\\Users\\dalto\\Desktop\\513.xlsx', 'C:\\Users\\dalto\\Desktop\\514.xlsx', 'C:\\Users\\dalto\\Desktop\\515.xlsx', 'C:\\Users\\dalto\\Desktop\\516.xlsx', 'C:\\Users\\dalto\\Desktop\\518.xlsx', 'C:\\Users\\dalto\\Desktop\\519.xlsx', 'C:\\Users\\dalto\\Desktop\\520.xlsx', 'C:\\Users\\dalto\\Desktop\\521.xlsx', 'C:\\Users\\dalto\\Desktop\\522.xlsx', 'C:\\Users\\dalto\\Desktop\\523.xlsx', 'C:\\Users\\dalto\\Desktop\\524.xlsx']
    
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
    startDate = datetime.strptime(dates["startDate"].split(" ")[0], "%Y-%m-%d")
    endDate = datetime.strptime(dates["endDate"].split(" ")[0], "%Y-%m-%d")

    #TODO: Interface with generating method
    #lst: results = BlakesClass.nameOfGenerationMethod(startDate, endDate)

    """
    Remove this line when the above work is implementd.
    You can test the flutter by changing what is in this list.
    True is the case when it works, a list of strings (specifically)
    File locations for when it fails. Just comment the one you don't
    want then restart the server.
    """
    #results = [True, "There were 86 total runs this period.", "This report includes runs 367 to 453.", "This report ranges from startDate to endDate"]
    results = ["Some error message!"]

    return jsonify(results)
