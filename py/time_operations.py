from unittest import TestCase
from datetime import tzinfo


class TzLocal(tzinfo):
    def __init__(self):
        from datetime import timedelta
        import time


        self.zonedelta = timedelta(seconds = -time.altzone) if time.daylight else timedelta(seconds=-time.timezone)
        self.name = time.tzname[time.daylight]

    def __repr__(self):
        return self.name

    def utcoffset(self, dt):
        return self.zonedelta

    def dst(self, dt):
        return self.zonedelta

    def tzname(self, dt):
        return self.name


def seconds_between(sec):
    import time
    import math

    start = time.time()
    time.sleep(sec)
    return math.ceil(time.time() - start)


def convert_12to24(time12):
    h, m, s = time12.split(':')
    h = int(h)
    if s.endswith('PM'):
        h = 12 if h == 12 else h + 12
    elif s.endswith('AM') and h == 12:
        h = 0
    return '{0:02}:{1}:{2}'.format(h, m, s[:-2])


class TestTime(TestCase):
    def test_convert_12to24(self):
        from datetime import time

        for hour in range(24):
            t = time(hour=hour, minute=0, second=0, tzinfo=TzLocal())
            time12 = t.strftime('%I:%M:%S%p')
            time24 = t.strftime('%H:%M:%S')
            self.assertEqual(time24, convert_12to24(time12))

    def test_strptime(self):
        from datetime import datetime as dt

        dt.strptime('Wed Nov 23 11:57:13 MSK 2016', '%a %b %d %H:%M:%S %Z %Y')
        dt.strptime('Wed Nov 23 11:57:13 MSK 2016', '%a %b %d %H:%M:%S %Z %Y')

        dt.strptime('22 May 2020 03:51:02.020065', '%d %b %Y %H:%M:%S.%f')
        dt.strptime('22 May 2020 15:35:43.956719 MSK +0300', '%d %b %Y %H:%M:%S.%f %Z %z')

        self.assertEqual(dt(year=2020, month=5, day=25, hour=3, minute=51, second=2), dt.strptime('25 May 2020 03:51:02 UTC', '%d %b %Y %H:%M:%S %Z'))


    def test_datetime_tz(self):
        from datetime import datetime as dt
        from datetime import timezone as tz
        from datetime import timedelta as td
        import time

        now = dt.now(TzLocal())
        print(now.strftime('%d %b %Y %H:%M:%S.%f %Z %z'))

        now = dt.now(tz(td(seconds=3600)))
        print(now.strftime('%d %b %Y %H:%M:%S.%f %Z %z'))

        now = dt.now(tz(td(seconds=3600), name='MY'))
        print(now.strftime('%d %b %Y %H:%M:%S.%f %Z %z'))

        now = dt.now(tz(td(hours=3, minutes=30), name='MY'))
        print(now.strftime('%d %b %Y %H:%M:%S.%f %Z %z'))


    def test_time_tz(self):
        import time

        format = '%d %b %Y %H:%M:%S %Z (UTC%z)'
        now = time.localtime()
        time_s = time.strftime(format, now)
        back = time.strptime(time_s, format)
        print(now, time_s, back)
