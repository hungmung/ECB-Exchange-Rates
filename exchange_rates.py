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

def strip_dates(data, start, end):
    """
    Strip dates before start date and after end date from a list
    
    Parameters:
        data  (list)     : List of dict elements.  One element must be 'dateEnd' in format YYYY/MM/DD.
        start (datetime) : earliest date for which informations is required
        end   (datetime) : latest (ost recent) date for which data is required
    Returns:
        data (list).     : stripped version of input list)
    """
    for element in list(data):
     if start:
        element_dt = datetime.date(
            int(element['dateEnd'].split('/')[2]),
            int(element['dateEnd'].split('/')[1]),
            int(element['dateEnd'].split('/')[0])
        )
        if element_dt < start:
            data.remove(element)
        continue
    if end:
      element_dt = datetime.date(
          int(element['dateEnd'].split('/')[2]),
          int(element['dateEnd'].split('/')[1]),
          int(element['dateEnd'].split('/')[0])
      )
      if element_dt > end:
        data.remove(element)
        continue
  return data

def clean_data(data):
    " Remove redundant dict entries from all elements of the input list "
  for x in data:
    del (x['currencyIso'])
    del (x['refCurrencyIso'])
    del (x['dateStart'])
  return data

def add_period_to_data(data):
  # Assume periods take to form yyyynn where nn is the reporting month starting at 1.
  # This implementation assumes the first reporting period start in April of each year
  for e in data:
    yyyy = int(e['dateEnd'].split('/')[2])
    mm = int(e['dateEnd'].split('/')[1])
    if mm <= 3:
      yyyy -= 1
      mm += 9
    else:
      mm -= 3
    e['period'] = "%d%02d" % (yyyy,mm)
  return data

def get_raw_data():
  base_url = "https://ec.europa.eu/budg/inforeuro/api/public/currencies/gbp"

  result = requests.get(base_url)
  if result.status_code != 200:
    print ("Error in getting results; " + results.status_code)
    return None
  return result.json()

def export_to_csv(data, file):
  import csv
  with open('exchange_rates.csv', 'w') as csvfile:
    fieldnames = ['period', 'dateEnd', 'amount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='unix')
    rtn = writer.writeheader()
    rtn = writer.writerows(data)
  return

ifdef __name__ == '__main__':
    start_date = "2018-09" #In format YYYY-MM or None (inclusive).  Represents to oldest date for which date is required
    end_date   = "2021-12" #In format YYYY-MM or None (inclusive). Represents most recent date for which data is required
    add_period = True # Un addtion to reporting months for exchange rates, also list accoring to reporting period

    if start_date: start_date = to_datetime(start_date)
    if end_date: end_date = to_datetime(end_date)
    if start_date and end_date and start_date > end_date:
        print ("Start date after end date")
        exit(1)

    data = get_raw_data()
    if start_date != None or end_date != None:
        data = strip_dates(data, start_date, end_date)
    if add_period:
        data = add_period_to_data(data)
    data = clean_data(data)
    export_to_csv(data, None)
    
    
