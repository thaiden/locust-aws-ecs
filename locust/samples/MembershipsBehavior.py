from locust import HttpLocust, TaskSet, task
from api.Api import Api
from api.Headers import Headers

import json
import AbstractTaskSet


class MembershipsBehavior(AbstractTaskSet):
    def __init__(self, parent):
        self.user = None
        self.room = None
        AbstractTaskSet.__init__(self, parent)

    @task
    def get_membership_list(self):
        headers = Headers.get_auth_json_header(self.user['token']['access_token'])

        self.client.get('/memberships', headers=headers)

    @task
    def create_memberships(self):
        headers = Headers.get_auth_json_header(self.user['token']['access_token'])
        data = {
            'roomId': '%s' % self.room['id'],
            'personEmail': Api.generate_email_address()
        }

        self.client.post('/messages', data=json.dumps(data), headers=headers)

    def on_start(self):
        self.user = Api.create_fake_user(display_name='Test User for Send Message')
        self.room = Api.create_room(title='Hello World', access_token=self.user.access_token)
