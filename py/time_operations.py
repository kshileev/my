from unittest import TestCase
from datetime import tzinfo, timedelta


class MSK(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=4)

    def dst(self, dt):
        return timedelta(hours=4)

    def tzname(self, dt):
        return "MSK"


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
    def setUp(self):
        super(TestTime, self).setUp()

    def test_convert_12to24(self):
        from datetime import time

        for hour in range(24):
            t = time(hour=hour, minute=0, second=0, tzinfo=MSK())
            time12 = t.strftime('%I:%M:%S%p')
            time24 = t.strftime('%H:%M:%S')
            self.assertEqual(time24, convert_12to24(time12))

    def test_strptime(self):
        from datetime import datetime

        with self.assertRaises(ValueError):  # bug in time zone
            datetime.strptime('Wed Nov 23 11:57:13 MSK 2016', '%a %b %d %H:%M:%S %Z %Y')
            datetime.strptime('Wed Nov 23 11:57:13 MSK 2016', '%a %b %d %H:%M:%S %Z %Y')

    def test_seconds_between(self):
        self.assertEqual(2, seconds_between(1))
