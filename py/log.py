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
        d['deployer-info'] = self._deployer_tag
        d['jenkins'] = self._jenkins_tag
        return json.dumps(d)


class JsonFilter(logging.Filter):
    def filter(self, record):
        return record.exc_text or '=' in record.message


class MyLogger(logging.Logger):
    def __init__(self, name):
        super(MyLogger, self).__init__(name)
        text_log_name, json_log_name = 'text.log', 'json.log'
        formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s [%(name)s]  %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(text_log_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        json_handler = logging.FileHandler(json_log_name)
        json_handler.setLevel(logging.DEBUG)
        json_handler.setFormatter(JsonFormatter())
        json_handler.addFilter(JsonFilter())

        self.setLevel(level=logging.DEBUG)
        self.addHandler(file_handler)
        self.addHandler(console_handler)
        self.addHandler(json_handler)

        logging.captureWarnings(True)


logger = MyLogger(__file__)


class TestLog(TestCase):
    def setUp(self):
        super(TestLog, self).setUp()

    def test_log(self):
        logger.info('message')
        logger.debug('message')
        logger.error('message')
        try:
            raise Exception('artificial exception')
        except Exception as ex:
            logger.exception(ex)
