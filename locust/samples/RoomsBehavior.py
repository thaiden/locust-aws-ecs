from locust import HttpLocust, TaskSet, task
from api.Api import Api
from api.Headers import Headers
from api.Utils import Utils

import json

import AbstractTaskSet


class RoomsBehavior(AbstractTaskSet):
    def __init__(self, parent):
        self.user = None
        self.room = None
        AbstractTaskSet.__init__(self, parent)

    @task
    def get_room_list(self):
        headers = Headers.get_auth_json_header(self.user.access_token)
        self.client.get('/rooms', headers=headers)

    @task
    def get_room_details(self):
        headers = Headers.get_auth_json_header(self.user.access_token)
        self.client.get('/rooms/%s' % self.room['id'], headers=headers)

    @task
    def create_room(self):
        headers = Headers.get_auth_json_header(self.user.access_token)
        data = {
            'title': 'Room %s is a good room' % Utils.randomString(10)
        }

        self.client.post('/rooms', data=json.dumps(data), headers=headers)

    @task
    def updateRoom(self):
        headers = Headers.get_auth_json_header(self.user.access_token)
        data = {
            'title': 'Room %s is a different room' % Utils.randomString(10)
        }

        self.client.put('/rooms/%s' % self.room['id'], data=json.dumps(data), headers=headers)

    def on_start(self):
        self.user = Api.create_fake_user(display_name='Test User for Create Room')
        self.room = Api.create_room(title='Hello World', access_token=self.user.access_token)
