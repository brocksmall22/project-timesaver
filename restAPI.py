from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Documents(Resource):
    def getLocations(self):
        data = request.get_json()
        print(data)
        return data

    def

class Display(Rescource):

    pass


api.add_resource(Documents, '/documents')

if __name__ == '__main__':
    app.run()