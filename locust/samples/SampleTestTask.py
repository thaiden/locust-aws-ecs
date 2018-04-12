"""
    This is sample locus test task
"""
from locust import task
from locust.exception import StopLocust
from api.Api import Api
from api.Headers import Headers

import AbstractTaskSet

import logging
import uuid


class SampleTestTask(AbstractTaskSet):
    """
    Any data created here is this task instance specific and is not shared between other instances of taskset
    """

    def __init__(self, parent):
        self.user = None
        self.room = None
        AbstractTaskSet.__init__(self, parent)

    def is_task_ready(self):
        """
        check to see if task is ready for execution
        :return: boolean
        """
        return self.user and self.room

    def on_start(self):
        """
        This locust framework defined way of preparing test context
        before task is executed, basic contract is that logic inside of
        on_start(self) method guaranteed to be executed before methods with
        @task annotation called

        :return: None
        """
        self.user = Api.create_fake_user('example-user-%s' % uuid.uuid4())
        if self.user:
            self.room = Api.create_room('Test room', self.user.access_token)


    @task
    def send_message(self):
        """
        this is an actual task executed by locust framework, you can have mutiple tasks within
        one task set, in that case if you want to have some form of controlling execution
        ration of those tasks, that can done via weight argument

            :Example
            @task(1)
            def func1(self):
                .....

            @task(2)
            def func2(self):
                .....

        func2 will be executed twice more often than func1

        To programmatically stop execution of taskset can be achieved by raising StopLocust exception
        :return: None
        """

        if self.is_task_ready():
            headers = Headers.get_auth_json_header(self.user.access_token)
            data = {
                'roomId': self.room['id'],
                'text': 'This is message from Locust task'
            }

            logging.debug('Headers user are: %s', headers)

            self.post(path='messages', data=data, headers=headers)
        else:
            raise StopLocust('Task is not ready')





