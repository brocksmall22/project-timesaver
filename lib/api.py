from flask import Flask, jsonify, request
import json

from flask.wrappers import Request

app = Flask(__name__)

@app.errorhandler(404)
def invalid_route():
    return(jsonify({"errorCode": 404, "message": "Route not found! Requested address was: " + Request.full_path}))

@app.route('/submit_reports', methods=["GET", "POST"])
def submit_reports():
    files = request.json

    #TODO: Interface with adding method
    # lst: results = DylansClass.nameOfIngestionMethod(files)

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

@app.route('/generate_report', methods=["GET", "POST"])
def generate_reports():
    dates = request.json
    print(dates)

    #TODO: Interface with generating method
    #lst: results = BlakesClass.nameOfGenerationMethod(dates)

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
