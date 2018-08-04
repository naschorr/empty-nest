## import json
import utilities

## Config
CONFIGS = utilities.load_config()

class NestStateEvent:
    def __init__(self, user, away_state):
        self._user = user
        self._away_state = away_state

    def __bool__(self):
        return (self.user != None and self.away_state != None)

    ## Properties

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        users = CONFIGS.get('users')
        print(users)
        if (value in users):
            self._user = value
        else:
            self._user = None
        print('user =', value)

    @property
    def away_state(self):
        return self._away_state

    @away_state.setter
    def away_state(self, state):
        if (state in ['home', 'away']):
            self._away_state = state
        else:
            self._away_state = None

    ## Methods

    # def to_json(self):
    #     return json.dumps({
    #         'user': self.user,
    #         'away_state': self.away_state
    #     })
