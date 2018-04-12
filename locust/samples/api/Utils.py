import random
import string
import os
import re


class Utils(object):
    @staticmethod
    def randomString(n):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    @staticmethod
    def random_int(a, b):
        return random.randint(a, b)

    @staticmethod
    def get_scopes(data):
        scopes = ''
        for scope in data:
            scopes += '%s ' % scope
        return scopes

    @staticmethod
    def get_env_var(key, default_value):
        value = default_value
        try:
            value = os.environ[key]
        except KeyError:
            pass
        return value

    @staticmethod
    def extract_link_info_from_request(headers):
        pattern = '.*(\/events.*)>;.rel'
        key = None
        if 'link' in headers.keys():
            key = 'link'
        elif 'Link' in headers.keys():
            key = 'Link'

        if key:
            value = headers[key]
            try:
                result = re.search(pattern, value)
                if result:
                    return result.group(1)
            except Exception, e:
                print 'Error occurred', str(e)
                pass
