from http.server import HTTPServer, BaseHTTPRequestHandler

import utilities
from request_parser import NestAwayRequestParser
from nest_manager import NestAwayManager

## Configs
CONFIGS = utilities.load_config()
REQUEST_PARSER = NestAwayRequestParser()
NEST_MANAGER = NestAwayManager()

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len)

        state = REQUEST_PARSER.parse(body)    # Safe(ish), valid json
        if (state):
            status_code, response_json = NEST_MANAGER.update_state(state)
            self.send_response(status_code, response_json)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
        else:
            self.send_response('400', '{\"error\": \"Malformed request, didn\'t contain valid \'user\' and \'away_state\' properties\"}')
            self.send_header("Content-Type", "application/json")
            self.end_headers()


class EmptyNest:
    def __init__(self):
        server_address = ('', CONFIGS.get('port', 80))
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.serve_forever()


if (__name__ == '__main__'):
    EmptyNest()
