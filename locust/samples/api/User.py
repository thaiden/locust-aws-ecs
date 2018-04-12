class User(object):
    def __init__(self, info):
        self.user_info = info

    @property
    def access_token(self):
        return str(self.user_info['token']['access_token'])

    @property
    def id(self):
        return str(self.user_info['user']['id'])

    @property
    def email(self):
        return str(self.user_info['user']['email'])

    def __repr__(self):
        return '%s' % self.user_info
