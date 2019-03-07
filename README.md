# ait-easytimetable
RESTful API built with Flask to provide an interface to AthloneIT class timetables.

## Usage

To request a timetable, you will need to send a GET request to the API, with the relevant course code as a `course_code` parameter. The URL structure should be as follows:

```shell
$ curl 'http://estilen.com/api/timetable?course_code={course_code}'
```

The API returns a JSON response with the following format:

```json
{
    "timestamp": "2019-03-07T21:21:37",
    "message": "success",
    "course_code": "course_code",
    "timetable_date": "2019-03-07T14:00:01",
    "timetable": {
        "Monday": [
            {
                "module_name": "Practical",
                "type": "Lab/Prac",
                "room": "W202",
                "time_start": "9:00",
                "time_end": "11:00",
                "lecturer": "John Doe"
            },
            {
                "module_name": "Lecture",
                "type": "Lecture",
                "room": "X103",
                "time_start": "11:00",
                "time_end": "12:00",
                "lecturer": "Jane Doe"
            }
        ],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": []
    }
}
```

Python quickstart example:

```python
import requests

response = requests.get("http://estilen.com/api/timetamble?course_code=AL_KSENG_B_4 A")
data = response.json()
timetable = data.get("timetable")
for day, modules in timetable.items():
    process(day, modules)
```

## Course list

A list of all supported departments and courses can be found [here](https://github.com/estilen/ait-easytimetable/blob/master/utils/departments.json).
