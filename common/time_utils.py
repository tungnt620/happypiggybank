import time
import datetime
import calendar


def timestamp():
    return int(time.time())


def timestamp_to_string(timestamp, format="%Y-%m-%d %H:%M:%S"):
    return datetime_to_string(timestamp_to_datetime(timestamp), format)


def today():
    return datetime.date.today()


def now():
    return datetime.datetime.now()


def utc_now():
    return datetime.datetime.utcnow()


# Return a date = day + a number of days
def add_day_to_date(day, add_days):
    return datetime.date.fromordinal(day.toordinal() + add_days)


# Return a datetime = now + a number of days
def add_day_to_datetime(now, add_days):
    return now + datetime.timedelta(days=add_days)


# Datetime to string, can use for date
def datetime_to_string(datetime, format="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(format)


# Convert datetime to utc
def datetime_to_utc(date_time):
    time_stamp = date_to_timestamp(date_time)
    return datetime.datetime.utcfromtimestamp(time_stamp)


def date_to_timestamp(date):
    return int(time.mktime(date.timetuple()))


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def get_last_day_of_month(month=None, year=None):
    td = today()
    if not month:
        month = td.month
    if not year:
        year = td.year

    return calendar.monthrange(year, month)[1]


def string_to_datetime(str, format='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.strptime(str, format)
