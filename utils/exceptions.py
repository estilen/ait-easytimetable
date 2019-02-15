class TimetableException(Exception):
    """Base class exception."""


class TimetableNotFound(TimetableException):

    def __init__(self, timetable_set):
        self.timetable_set = timetable_set
        super().__init__(f'timetable set not found: \'{timetable_set}\'')


class RequestedDayNotSupported(TimetableException):

    def __init__(self, week_day):
        self.week_day = week_day
        super().__init__(f'day of the week invalid or not supported: \'{week_day}\'')


class TimetableNotAvailable(TimetableException):
    """The timetable.ait.ie website returned unexpected content or
    is unavailable."""
