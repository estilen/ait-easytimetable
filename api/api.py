from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from resources import TimetableResource


app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(TimetableResource, "/api/timetable")
