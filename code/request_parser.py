import json

from nest_state_event import NestStateEvent


class NestAwayRequestParser:
    def parse(self, body):
        request_json = json.loads(body)

        ## Trim out any unwanted properties
        state = NestStateEvent(request_json.get('user'), request_json.get('away_state'))

        if (not state):
            return None

        return state