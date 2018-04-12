from locust import HttpLocust, TaskSet, task, InterruptTaskSet

from samples.SampleTestTask import SampleTestTask


class HydraBehavior(TaskSet):
    tasks = [SampleTestTask]


class WebsiteUser(HttpLocust):
    task_set = HydraBehavior
    min_wait = 0
    max_wait = 5000
