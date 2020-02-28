class Curl:
    def __init__(self, logger, via_curl=None):
        import urllib3

        self.via_curl = via_curl
        if not self.via_curl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.logger = logger

    def __repr__(self):
        return 'via curl' if self.via_curl else 'via requests'

    def curl_get(self, url, uname=None, passwd=None, headers=None):
        import requests

        if self.via_curl:
            cmd = f'curl -i -k -X get {headers} '
            return self.via_curl.cmd_exec(cmd)
        else:
            auth = (uname, passwd) if uname else None
            return self.process_response(requests.get(url, auth=auth, headers=headers, verify=False))

    def process_response(self, resp):
        self.to_curl(resp=resp)
        if resp.status_code == 200:
            return resp
        else:
            raise RuntimeError(f'{resp.request.method} failed')

    def to_curl(self, resp):
        request = resp.request
        headers = ' '.join([f'-H "{k}: {v}"' for k, v in sorted(request.headers.items()) if k not in ['Accept', 'Accept-Encoding', 'Connection', 'Content-Length', 'Content-Type', 'User-Agent']])
        if request.body:
            body = f'-d "{request.body.decode("utf-8")}"' if isinstance(request.body, bytes) else f'-d "{request.body}"'
        else:
            body = ''
        self.logger.info(f'curl -i -k -X {request.method} {headers} {body} {request.url}\n{resp.text}')
