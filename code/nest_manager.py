import http.client
import json
import os
from urllib.parse import urlparse

import utilities

## Config
CONFIGS = utilities.load_config()

class NestAwayManager:
    def __init__(self):
        self.token = utilities.load_json_from_root(CONFIGS.get('token_path'))['token']
        self.url = '/structures/{}'.format(CONFIGS.get('structure_id'))
        self.connection = http.client.HTTPSConnection("developer-api.nest.com")
        self.headers = {'authorization': "Bearer {0}".format(self.token)}

        self.states = self.load_states()


    def load_states(self):
        try:
            with open(os.sep.join([utilities.get_root_path(), CONFIGS.get('state_path')])) as fd:
                return json.loads(fd.read());
        except json.JSONDecodeError:
            ## Load some sort of default
            output = {}
            for user in CONFIGS.get('users', []):
                output[user] = 'home'

            return output

        
    def save_states(self):
        with open(os.sep.join([utilities.get_root_path(), CONFIGS.get('state_path')]), 'w') as fd:
            fd.write(json.dumps(self.states, indent=4))


    def calculate_away_state(self):
        away_state = 'away'
        for value in self.states.values():
            if (value == 'home'):
                away_state = value
                break

        return away_state


    def update_state(self, state_event):
        before_state = self.calculate_away_state()

        self.load_states()
        self.states[state_event.user] = state_event.away_state
        self.save_states()

        after_state = self.calculate_away_state()

        if (before_state != after_state):
            payload = json.dumps({'away': after_state})
            self.connection.request('PUT', self.url, payload, self.headers)
            response = self.connection.getresponse()

            if (response.status == 307):  # indicates a redirect is needed
                redirect_location = urlparse(response.getheader('location'))
                connection = http.client.HTTPSConnection(redirect_location.netloc)
                connection.request('PUT', self.url, payload, self.headers)
                response = connection.getresponse()
                if (response.status != 200):
                    return response.status, response.reason
            elif (response.status < 200 or response.status >= 300):
                return response.status, response.reason
            
            return 204, 'Nest updated successfully.'

        else:
            return 200, 'No Nest changes necessary.'
