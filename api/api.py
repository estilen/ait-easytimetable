from flask import Flask
from flask_restplus import Api

from resources import TimetableResource


app = Flask(__name__)
api = Api(app)

api.add_resource(TimetableResource, "/api/timetable")
