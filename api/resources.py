import glob
import json
import os
import re
import urllib.parse
from datetime import datetime

from flask import request
from flask_restplus import Resource


def quote(*args, **kwargs):
    """Encodes each underscore in the course code string.

    Implementation adapted from the following StackOverflow answer.
    https://stackoverflow.com/a/37529885/7073884
    """
    encoded_course_code = urllib.parse.quote(*args, **kwargs)
    return re.sub(r"_", "%5F", encoded_course_code)


class TimetableResource(Resource):

    def get(self):
        course_code = request.args.get("course_code")
        if course_code is None:
            return {"timestamp": datetime.now().isoformat(timespec='seconds'),
                    "message": "request missing course code"
            }, 400

        timetables = glob.glob("/var/lib/easytimetable/timetables/*.json")
        if not timetables:
            return {"timestamp": datetime.now().isoformat(timespec='seconds'),
                    "message": "cannot locate a valid timetable"
            }, 500

        latest_timetable = max(timetables, key=os.path.getctime)
        with open(latest_timetable) as f:
            data = json.load(f)
            timetable = data.get(quote(course_code))

        if timetable is None:
            return {"timestamp": datetime.now().isoformat(timespec='seconds'),
                    "message": "requested timetable does not exist",
                    "course_code": course_code
            }, 400

        if timetable == {}:
            return {"timestamp": datetime.now().isoformat(timespec='seconds'),
                    "message": "cannot find requested timetable",
                    "course_code": course_code
            }, 200

        return {"timestamp": datetime.now().isoformat(timespec='seconds'),
                "message": "success",
                "course_code": course_code,
                "timetable_date": data["timestamp"],
                "timetable": timetable
        }, 200
