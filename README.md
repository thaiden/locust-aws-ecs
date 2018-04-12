# Readme

Its simple!

## Prerequisites 
1. Make sure python is installed
2. Make sure latest docker & docker-compose installed
2. run ```pip -r requirements.txt install``` to install needed python modules


## Creating your first locust TaskSet

Please refer to locust/samples/AbstractTaskSet.py on how to write TaskSet's for locust

```python

class SampleTestTask(AbstractTaskSet):
    
    def __init__(self, parent):    
        AbstractTaskSet.__init__(self, parent)
        
    @task
    def do_something(self):
        pass
```

To make sure your new TaskSet is running, locate /test-scenarios/locustfile.py, and replace task in here with 
name of your TaskSet class

```python
class HydraBehavior(TaskSet):
    tasks = [<put_your_class_name_here>]
```


## Configration

All configuration is stored in 2 files under /test-scenarios

 - config.loada.json - Load test env
 - config.local.json - and local run
 
 choice of file is controlled via `.evn` file
 
```
TARGET_URL=http://some-service/api/rooms
RUNNING_ENV=loada
```

 - **TARGET_URL** is what url locust going to hit
 - **RUNNING_ENV** is env its going to run against
 
**IMPORTANT** - See how RUNNING_ENV is point to **loada**, that is basically prefix for which conf file to select, for more info see
/locust/samples/api/Config.py


## How to start Locust
to start locust with webserver in:
 * *attached form* - run ```docker-compose up --build``` to point to remote load test env
 * *detached form* - pass ```-d``` flag after ```up``` command

 For more commands use **docker-compose help**


More information can be found in official locust [documentation](https://docs.locust.io/en/latest/writing-a-locustfile.html) 

### Master/Slave setup
Check README in **locust-aws-ecs** folder

## How to start or stop Test Tasks
see usage of ```run-swarm.py```
 * **start** -> ```run-swarm.py --action start```
 * **stop** -> ```run-swarm.py --action stop```

## How to control load
Load applied to server is controlled by increasing/decreasing number for **locust_ccount** & **hatch_rate**.

to see what locust_count & hatch_rate are and how they are use see [locust doc](http://docs.locust.io/en/stable/writing-a-locustfile.html?highlight=hatch) or ```$locust --help``` 

## Retrieve results
Use ```run-swarm.py --action results```, all files are placed under **results** folder and in subfolder which represents time script was executed(seconds)

## Test data
To generate test data take a look at README in /test-data folder