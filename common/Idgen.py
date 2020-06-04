# - * - encoding: utf - 8 -*-
import socket
import threading
import random
import json
import time
from loguru import logger
import time
import datetime
import requests
from locust import task,TaskSet,HttpLocust
from time import ctime
def IDGenegator():
    re = requests.post(
        headers = {
            "Content-Type": "text/html;charset=UTF-8"
        },
        url="http://192.168.2.81:8087/SettMerchant/pfyhNotify"
    )
    result = re.status_code
    logger.info(result)

class UserBehavior(TaskSet):

    def on_start(self):
        self.start_time = ctime()
        return self.start_time

    @task(weight=1)
    def id(self):
        IDGenegator()



class WebUserLocust(HttpLocust):
    weight = 1
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
    # host = '183.57.43.214:8999'#product
    host = "192.168.2.81:8087"
