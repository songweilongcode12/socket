import requests
from loguru import logger
import json
import random
from locust import task,TaskSet,HttpLocust
def submit():
    '''
    公众号下单api
    '''
    re_url = 'http://test69.qtopay.cn/diancan-api/order/submit'
    headers = {
                "Accept": "application/json, text/plain, */*",
                "token":"3ffbdb3b7ae04c9f8573bab3f50f0db1"
                }
    order_data ={
                "remark": "",
                "userVoucher": "",
                "submitOrderGoodReqList": [{"goodsId": 1040, "total": 1, "submitOrderGoodOptionReqList": [1485], "submitOrderGoodSetReqList": []}],
                "storeId": "117",
                "couponNo": "255817815480962536",
                "address": "测试结果",
                "diningMode": 2,
                "mileTime": "立即送出",
                "mobile": "15867888555",
                "username": "测试",
                "orderType": "3"
                }
    re = requests.post(
                        url = re_url,
                        data = json.dumps(order_data),
                        headers = headers
                       )
    logger.info(re.text)

def goodsname():
    goods = random.randint(9999,999999999)
    names = 'song_testing' + str(goods)
    # logger.info(names)
    return names
def price():
    account = str(random.randint(1,200)) + '.' + str(random.randint(0,99))
    # logger.info(account)
    return account
def loginclient():
    headers = {
        "Content-Type": "application/json",
    }
    login_data = {
                "phone":"18699081687",
                "password": "123456",
                "code": "0721",
                "key": "114bdff2-c0c5-47d9-a7ab-75e0d3331156",
                "areaCode": "+86"
            }
    log_url = 'http://test19.qtopay.cn/wx/auth/login'
    re = requests.post(
                        url = log_url,
                        data=login_data,
                        headers = headers
                )
    logger.info(re.text)
def create_goods():
    # url = 'http://test19.qtopay.cn/admin/goods/create'
    url ='http://admin.bmall.com.hk/admin/goods/create'
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
               "Admin-Token":"9chrmcvpnrlzzni4yzvqio5qao10j03y"
             }
    logger.info(create_data)
    re = requests.post(
                        url=url,
                        data=json.dumps(create_data),
                        headers=headers
                    )
    logger.info(re.text)
    logger.info(create_data)
def getGoodslist():
    url = 'http://admin.bmall.com.hk/wx/goods/list?page=1&size=10000&classifyId='
    # data = {
    #     "page":1,
    #     "size":1000,
    # }
    headers = {
                "Content-Type": "application/json",
               "Admin-Token":"9chrmcvpnrlzzni4yzvqio5qao10j03y"
             }
    re = requests.get(
        url=url,
        headers=headers
    )
    logger.info(re.json())
# getGoodslist()
class UserBehavior(TaskSet):


    @task(weight=1)
    def creategoods(self):
        getGoodslist()


class WebUserLocust(HttpLocust):
    weight = 1
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
    host ='admin.bmall.com.hk'
