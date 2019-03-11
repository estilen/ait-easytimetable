import functools
import re
from datetime import datetime as dt
from time import strftime

import requests
from bs4 import BeautifulSoup

import exceptions


TIMETABLE_URL = "http://timetable.ait.ie/reporting/textspreadsheet;student+set;id;{}?t=student+set+textspreadsheet&days=1-5&=&periods=3-20&=student+set+textspreadsheet&weeks={}&template=student+set+textspreadsheet"  # noqa


class Timetable:
    """Abstract interface class to access AthloneIT college timetables."""

    day_index = {"Monday": 0,
                 "Tuesday": 1,
                 "Wednesday": 2,
                 "Thursday": 3,
                 "Friday": 4}

    def __init__(self, course_code,
                 week_number=None, week_starting="20180827", session=None):
        self.course_code = course_code.upper()
        self._week_number = week_number
        self._week_starting = week_starting
        self._session = session or requests.Session()

    def week_number(self):
        """Adapted this StackOverflow answer to return correct week number.
        https://stackoverflow.com/a/51940001/7073884
        """
        if self._week_number:
            return self._week_number
        started_week = dt.strptime(self._week_starting, "%Y%m%d")
        current_week = dt.strptime(strftime("%Y%m%d"), "%Y%m%d")
        return (current_week - started_week).days // 7 + 1

    @property
    def _url(self):
        """Build the URL."""
        return TIMETABLE_URL.format(self.course_code, self.week_number())

    def _request_timetable(self):
        try:
            return self._session.get(self._url)
        except requests.exceptions.ConnectionError:
            raise exceptions.TimetableNotAvailable()

    @property
    @functools.lru_cache(maxsize=1)
    def week(self):
        """Return a list of bs4.element.Tag objects, where each item contains
        data relevant to each module.
        """
        response = self._request_timetable()
        soup = BeautifulSoup(response.content, "lxml")
        if response.status_code == 400:
            raise exceptions.TimetableNotFound(soup.select("b")[-1].text)
        return soup.select("table[cellpadding]")

    def _parse_lecturer_name(self, string):
        if "ZZZ" in string:
            return string
        if ";" in string:
            names = [[n.strip().capitalize()
                      for n in name.split(",")][::-1]
                     for name in string.split(";")]
            return "; ".join([" ".join(name) for name in names])
        return " ".join([n.strip().capitalize()
                         for n in string.split(",")][::-1])

    def _parse_room_number(self, room):
        match = re.match(r"[A-Z]\d{2,4}", room)
        return room if not match else match.group(0)

    def _parse_daily_timetable(self, data):
        """Extract data for individual modules."""
        module = {}
        module["module_name"] = data[0].text
        module["type"] = "Lecture" if data[2].text == "Lec" else data[2].text
        module["room"] = self._parse_room_number(data[7].text.strip())
        module["time_start"] = data[3].text
        module["time_end"] = data[4].text
        module["lecturer"] = self._parse_lecturer_name(data[8].text)
        return module

    def _insert_breaks(self, day):
        copy = day[:]
        offset = 0
        for i in range(len(copy) - 1):
            end = copy[i]["time_end"]
            # Skip iteration if two modules are going ahead at the same time
            if end == copy[i + 1]["time_end"]:
                continue
            start = copy[i + 1]["time_start"]
            delta = dt.strptime(start, "%H:%M") - dt.strptime(end, "%H:%M")
            if delta:
                offset += 1
                missing_break = {"type": "Break",
                                 "time_start": end,
                                 "time_end": start
                                 }
                day.insert(i + offset, missing_break)
        return day

    def daily_timetable(self, requested_day=None):
        if requested_day is None:
            requested_day = strftime("%A")
        if requested_day not in self.day_index:
            raise exceptions.RequestedDayNotSupported(requested_day)
        index = self.day_index[requested_day]

        timetable = [self._parse_daily_timetable(row.select("td"))
                     for row in self.week[index].select("tr")[1:]]
        self._insert_breaks(timetable)
        return timetable

    def weekly_timetable(self):
        return {day: self.daily_timetable(day) for day in self.day_index}
