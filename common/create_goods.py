# - * - encoding: utf - 8 -*-
import socket
import threading
import requests
import random
import json
import time
from loguru import logger
import time
import datetime
import logging
from locust import task,TaskSet,HttpLocust
from time import ctime
def goodsname():
    goods = random.randint(1,2000)
    names = 'song_testing' + str(goods)
    logger.info(names)
    return names
def price():
    account = str(random.randint(1,200)) + '.' + str(random.randint(0,99))
    logger.info(account)
    return account
# def login():
#     headers = {
#         "Content-Type": "application/json",
#     }
#     login_data = {
#                 "phone":"18699081687",
#                 "password": "123456",
#                 "code": "0721",
#                 "key": "114bdff2-c0c5-47d9-a7ab-75e0d3331156",
#                 "areaCode": "+86"
#             }
#     log_url = 'http://test19.qtopay.cn/wx/auth/login'
#     re = requests.post(
#                         url = log_url,
#                         data=login_data,
#                         headers = headers
#                 )
#     logger.info(re.text)
def create_phone():
    phone_list = ['139','186','137','152','136','133','158','188','135','153','152']
    nums = '0123456789'
    for i in range(100):
        phone = random.choice(phone_list) + "".join(random.choice(nums)for i in range(8))
        print(phone)
    return phone
def create_goods():
    url = 'http://test19.qtopay.cn/admin/goods/create'
    create_data = {
                    "goods": {
                                "detail": "<p>测试数据，测哈数据</p>",
                                "country": "101",
                                "unit": "",
                                "picUrl": "https://kuajingdianshang.oss-cn-shenzhen.aliyuncs.com/gwmfpsj0fape6uf27erb4kn7yqkk.png",
                                "gallery": ["{\"image\":\"https://kuajingdianshang.oss-cn-shenzhen.aliyuncs.com/e76h7c3c3q3uo6pox4i804rxc0ao.png\",\"type\":\"image/png\"}"],
                                "medias": [],
                                "media": [],
                                "name":goodsname(),
                                "isNew": False,
                                "isHot": False,
                                "firstUnit": "",
                                "secUnit": "",
                                "firstNum": "",
                                "secNum": "",
                                "quarantineNo": "",
                                "customsRecordNo": "",
                                "customsClassificationNo": "",
                                "ncadCode": "",
                                "netWeight": "",
                                "grossWeight": "",
                                "shipmentRegion": "0",
                                "counterPrice": price(),
                                "retailPrice": price(),
                                "keywords": "123",
                                "categoryId": 1036011,
                                "classifyId": 1181001,
                                "brandId": 1046018,
                                "supplierId": 38,
                                "brief": "测试数据，测哈数据"
                            },
                    "specifications": [{
                        "specification": "规格",
                        "value": "标准",
                        "picUrl": ""
                    }],
                    "products": [{
                        "id": 0,
                        "specifications": ["标准"],
                        "price":  price(),
                        "taxFlag": 1,
                        "incomeTax": price(),
                        "number": 0,
                        "url": "",
                        "goodsSn": "",
                        "netWeight":  price(),
                        "grossWeight": price(),
                        "specificationType": "",
                        "freeShipping": 1,
                        "postage":  price(),
                        "supplyPrice":  price()
                    }],
                    "attributes": []
                }
    headers = {
                "Content-Type": "application/json",
               "Admin-Token":"rni5rgy3jjch1yq5tchklbnwfbclzh0u"
             }
    logger.info(create_data)
    re = requests.post(
                        url=url,
                        data=json.dumps(create_data),
                        headers=headers
                    )
    logger.info(re.text)
    logger.info(create_data)
def goodsIds():
    goodsId = 1182316
    goodsIds = goodsId - 1
    return str(goodsIds)
def shangjia():

    url1 = 'http://test19.qtopay.cn/admin/goods/onsale?'
    data = {
        "goodsId": goodsIds()

    }
    headers = {
        "Content-Type": "application/json",
        "Admin-Token": "rni5rgy3jjch1yq5tchklbnwfbclzh0u"
    }
    re = requests.get(url=url1,params=data,headers=headers)
    logger.info(re.text)
# shangjia()
class UserBehavior(TaskSet):

    def on_start(self):
        self.start_time = ctime()
        return self.start_time

    @task(weight=1)
    def CreditCardSecondsToTransactions(self):
        create_goods()
        shangjia()
        time.sleep(4)


    def On_end(self):
        self.end_time = ctime()
        return self.end_time




class WebUserLocust(HttpLocust):
    weight = 1
    task_set = UserBehavior
    min_wait = 30000
    max_wait = 50000
    # host = '183.57.43.214:8999'#product
    # host = "192.168.2.147:8948"

# create_phone()

def create_counter():
    def increase():
        n = 10
        while True:
            n = n+1
            yield n
            it = increase()
            def counter():
                return next(it())
            return counter
create_counter()