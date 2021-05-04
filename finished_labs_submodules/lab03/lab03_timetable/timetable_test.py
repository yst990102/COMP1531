from timetable import timetable
from datetime import date, time, datetime

def test_normal():
    assert (timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)])) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_empty_date():
    assert (timetable([], [time(14,10), time(10,30)])) == []

def test_empty_time():
    assert (timetable([date(2019,9,27), date(2019,9,30)], [])) == []
