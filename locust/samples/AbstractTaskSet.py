import json
import logging

from locust import TaskSet, InterruptTaskSet

success_status_codes = [200, 201, 204]


def validate_response(response, headers):
    if response.status_code not in success_status_codes:
        logging.warn('Error invoking request, TrackingId: %s, error: %s, request.status: %s', headers['TrackingId'],
                     response.text, response.status_code)
    return response


class AbstractTaskSet(TaskSet):
    def __init__(self, parent):
        TaskSet.__init__(self, parent)

    def post(self, path, data, headers):
        """
        http POST to TARGET_URL
        """
        return validate_response(
            self.client.post(path, data=json.dumps(data), headers=headers, verify=False), headers)

    def get(self, path, headers, group=None):
        """
        http GET to TARGET_URL
        """
        if group:
            return validate_response(self.client.get(path, name=group, headers=headers), headers)
        else:
            return validate_response(self.client.get(path, headers=headers), headers)

    def delete(self, path, headers, group):
        """
        http DELETE to TARGET_URL
        """
        return validate_response(self.client.delete(path, name=group, headers=headers), headers)
