import logging
from unittest import TestCase


class JsonFormatter(logging.Formatter):
    def __init__(self):
        import os

        self._jenkins_tag = os.getenv('BUILD_TAG', 'no_jenkins')
        self._deployer_tag = 'not implemented'
        super(JsonFormatter, self).__init__()

    def format(self, record):
        import re
        import json

        def split_pairs():
            for key_value in re.split(pattern=';', string=record.message):  # 'a=b  ; c=d=43 ; k=5' will produce {'a':'b', 'c': 'd=43', 'k':5}
                if '=' in key_value:
                    key, value = key_value.split('=', 1)
                    key = key.strip()
                    if not key:
                        continue
                    try:
                        value = int(value)
                    except ValueError:
                        value = value.strip()
                        if '@timestamp' not in key:
                            value = value.replace('-', '')
                            value = value.replace(':', '')
                    d[key] = value

        d = {}
        if record.exc_text:
            d['EXCEPTION'] = record.exc_text.replace('\n', '')
        split_pairs()
        if '@timestamp' not in d:
            d['@timestamp'] = self.formatTime(record=record, datefmt="%Y-%m-%dT%H:%M:%S.000Z")
        d['name'] = record.name
        return json.dumps(d)


class MainLogFormatter(logging.Formatter):
    def format(self, record):
        return self._fmt.format(time='' if '+-' in record.msg else self.formatTime(record, datefmt=self.datefmt), msg=record.msg).strip()


class MyFilter(logging.Filter):
    def __init__(self, name):
        super(MyFilter, self).__init__(name)
        self.func_name = name

    def filter(self, record):
        return record.funcName == self.func_name


formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(funcName)s %(message)s')

console_h = logging.StreamHandler()
console_h.setLevel(logging.DEBUG)
console_h.addFilter(MyFilter('test_log1'))
console_h.setFormatter(MainLogFormatter(fmt='{time} {msg}', datefmt='%b%d %H:%M:%S'))

file_h = logging.FileHandler('a_text.log', mode='w')
file_h.setLevel(logging.DEBUG)
file_h.addFilter(MyFilter('test_log2'))
file_h.setFormatter(formatter)

json_h = logging.FileHandler('a_json.log', mode='w')
json_h.setLevel(logging.DEBUG)
json_h.setFormatter(JsonFormatter())

logger = logging.getLogger('TEST')
logger.setLevel(level=logging.DEBUG)
logger.addHandler(file_h)
logger.addHandler(console_h)
logger.addHandler(json_h)

logging.captureWarnings(True)


class TestLog(TestCase):
    def setUp(self):
        super(TestLog, self).setUp()

    def test_log_exception(self):
        try:
            raise Exception('exception')
        except Exception as ex:
            logger.exception(ex)

    def test_log_simple(self):
        logger.info('info')
        logger.debug('debug')
        logger.error('error')

    def test_log_via_get_logger(self):
        log = logging.getLogger('TEST')
        log.info('info')
