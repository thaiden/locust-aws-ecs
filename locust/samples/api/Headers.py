import uuid

tacking_id_template = 'TEST_TRACKING_ID_%s'


class Headers(object):

    @staticmethod
    def get_auth_json_header(token):
        headers = Headers.get_json_header()
        headers['Authorization'] = 'Bearer %s' % token

        return headers

    @staticmethod
    def get_json_header():
        headers = {
            'content-type': 'application/json',
            'TrackingId': tacking_id_template % uuid.uuid4()
        }
        return headers

    @staticmethod
    def get_url_form_header():
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'TrackingId': tacking_id_template % uuid.uuid4()
        }
        return headers
