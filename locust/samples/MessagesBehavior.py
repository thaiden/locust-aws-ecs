from locust import HttpLocust, TaskSet, task
from api.Api import Api
from api.Headers import Headers
from api.Utils import Utils

import json
import AbstractTaskSet


class MessagesBehavior(AbstractTaskSet):
    def __init__(self, parent):
        self.user = None
        self.room = None
        AbstractTaskSet.__init__(self, parent)

    @task
    def get_messages(self):
        headers = Headers.get_auth_json_header(self.user.access_token)

        self.client.get('/messages', headers=headers)

    @task
    def send_messages(self):
        headers = Headers.get_auth_json_header(self.user)
        data = {
            'roomId': '%s' % self.room['id'],
            'text': 'Hello World %s' % Utils.randomString(10)
        }

        self.client.post('/messages', data=json.dumps(data), headers=headers)

    def on_start(self):
        self.user = Api.create_fake_user(display_name='Test User for Send Message')
        self.room = Api.create_room(title='Hello World', access_token=self.user.access_token)
