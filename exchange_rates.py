import requests
import json
import datetime
import unittest

def to_datetime(date_string):
    """
    Convert an input dare string in ISO8601 format (YYYY-MM) into a datetime object,
    and then change the date to the last day of the month since this is needed for H2020
    reporting.
    On success: datetime object returned
    On Failure: raise an assertion exception
    """
    import re
    import calendar
    
    assert re.match("\d{4}\-\d{2}", date_string, re.ASCII) != None, "Incorrect date format passed to to_datetime"
    yyyy = int(date_string.split('-')[0])
    mm = int(date_string.split('-')[1])
    dd = 1
    dt = datetime.date(yyyy,mm,dd)
    dt = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
    return dt

class TestDateMethods(unittest.TestCase):
    def test_valid(self):
        self.assertIsNotNone(to_datetime('2020-10'))
