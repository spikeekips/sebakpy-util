import time
import datetime


def iso8601now():
    formatted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tz = str.format('{0:+06.2f}', float(time.timezone) / 3600)
    return formatted + tz
