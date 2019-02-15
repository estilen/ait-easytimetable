import json
import time
import os
from datetime import datetime

import agent
from exceptions import TimetableNotFound

with open("departments.json") as f:
    data = json.load(f)

timetable = {"timestamp": datetime.now().isoformat(timespec='seconds')}
for department, courses in data.items():
    for course, course_code in courses.items():
        try:
            t = agent.Timetable(course_code)
            timetable[course_code] = t.weekly_timetable()
        except TimetableNotFound:
            timetable[course_code] = {}

# TODO: Multiprocessing to download timetable dump
timestamp = time.strftime("%Y%m%d-%H%M")
path = os.path.expanduser('~')
with open(f"{path}/timetables/timetable-{timestamp}.json", "w") as f:
    json.dump(timetable, f, indent=4)
