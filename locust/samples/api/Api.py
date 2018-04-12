from Config import Config
from Headers import Headers
from User import User

import requests
import json
import logging
import datetime
import random
import uuid

test_service_name = 'testServiceName'


class Api(object):

    @staticmethod
    def create_fake_user(display_name):
        data = {
            'user': {
                'id': '%s' % uuid.uuid4(),
                'email': '%s' % Api.generate_email_address(),
                'displayName': '%s' % display_name

            },
            'token': {
                'access_token': '%s' % uuid.uuid4()
            }
        }

        return User(data)

    @staticmethod
    def generate_email_address():
        now = datetime.datetime.now()
        rand = random.randint(1, 9999)
        email = 'test-group-{year}{month}{day}-{hour}{minute}{second}-{random}@test.example.com'.format(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            random=rand)

        return email

    @staticmethod
    def create_room(title='Default Title', access_token=None):
        headers = Headers.get_auth_json_header(access_token)
        data = {
            'title': title
        }

        return Api.post(
            url='%s/rooms' % Config.get('services')[test_service_name],
            data=json.dumps(data),
            headers=headers)

    @staticmethod
    def get_membership(room_id, access_token=None):
        headers = Headers.get_auth_json_header(access_token)

        response = requests.get(
            url='%s/memberships?roomId=%s' % (Config.get('services')[test_service_name], room_id),
            headers=headers)

        if 200 <= response.status_code < 300:
            logging.debug('Success')
        else:
            logging.error('Failed with error: %s', response.text)

    @staticmethod
    def create_membership(creator, room, new_member):
        headers = Headers.get_auth_json_header(creator.access_token)
        data = {
            'roomId': '%s' % room['id'],
            'personEmail': new_member.email
        }

        return Api.post(
            url='%s/memberships' % Config.get('services')[test_service_name],
            data=json.dumps(data),
            headers=headers)

    @staticmethod
    def delete_membership(user, membership):
        headers = Headers.get_auth_json_header(user.access_token)

        response = requests.delete(
            url='%s/memberships/%s' % (Config.get('services')[test_service_name], membership['id']),
            headers=headers)

        if 200 <= response.status_code < 300:
            logging.debug('Success')
        else:
            logging.error('Failed with error: %s', response.text)

    @staticmethod
    def post_message(token, room_id, email, message):
        template = '<@personEmail:%s> %s'

        headers = Headers.get_auth_json_header(token)
        data = {
            'roomId': '%s' % room_id,
            'markdown': template % (email, message)
        }

        return Api.post(url='%s/messages' % Config.get('services')[test_service_name], data=data, headers=headers)

    @staticmethod
    def post(url, data, headers):
        response = requests.post(url=url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logging.warning('failed to execute post %s' % response.text)

    @staticmethod
    def get(url, headers):
        response = requests.get(url=url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logging.warning('failed to execute get %s' % response.text)
