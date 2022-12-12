from q9 import timetable

def test_dryrun():
	assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) \
	  == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), \
	      datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]
