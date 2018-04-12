from locust import HttpLocust, TaskSet, task, InterruptTaskSet

from samples.SampleTestTask import SampleTestTask


class LocustBehavior(TaskSet):
    tasks = [SampleTestTask]


class WebsiteUser(HttpLocust):
    task_set = LocustBehavior
    min_wait = 0
    max_wait = 5000
