FROM tha1den/locust:8.0

ADD ./locust /locust

ENV RUNNING_ENV $RUNNING_ENV 
ENV PYTHONPATH $PYTHONPATH:/locust
ENV SCENARIO_FILE /locust/locustfile.py