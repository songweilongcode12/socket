import requests
import json
import hashlib
from loguru import logger
from common.md532 import md5
def md5(data):
    key ='78908DDDC2B63AC2E0530100007FF293'
    h1 = hashlib.md5()
    data1 = json.dumps(data,separators=(',',':'))
    data2 = str(key) + str(data1)
    logger.info(data1)
    # print(data1)
    h1.update(data2.encode("utf-8"))
    result = h1.hexdigest()
    logger.info(result)
    return result
def DiscountAmountCalculation():

    '''
    优惠券订单核销明细查询接口(1132)
    :return:
    '''
    try:
        url = 'http://192.168.2.239:8767/gateway/exterfaceInvoke.json'
        requestData = {
            "pageIndex": 1,
            "pageSize": 11,
            "shopId": "86000224",
            "thresholdType":"4"
        }
        data = {
            'requestData': requestData,
            "appId": "123456",
            "requestType": "1132",
            "dataSign": md5(data=requestData),

        }
        # logger.info(data)
        headers = {
            "Content-Type": "applications/json",
            "language": "2"
        }
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        responce = re.json()
        logger.info(responce)
        couponNo = responce['data']['list'][0]['couponNo']
        return couponNo
    except Exception as e:
        logger.info(e)
def CouponwriteoffStatistics():
    '''
    优惠券核销统计汇总查询接口(1133)
    :return: 
    '''
    try:
        url = 'http://192.168.2.239:8767/gateway/exterfaceInvoke.json'
        requestData = {
            "pageIndex": 1,
            "pageSize": 30,
            "shopId": "86000224",
            "thresholdType":"1"
        }
        data = {
            'requestData': requestData,
            "appId": "123456",
            "requestType": "1133",
            "dataSign": md5(data=requestData),
        }
        logger.info(data)
        headers = {
            "Content-Type": "applications/json",
            "language": "0"
        }
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.info(re.text)
        logger.info(re.headers)
    except Exception as e:
        print(e)

def SearchByNumber():
    '''
    根据劵编号查询劵信息、活动信息、门店信息(1134)
    :return:
    '''
    try:
        url = 'http://192.168.2.239:8767/gateway/exterfaceInvoke.json'
        requestData = {
            "couponNo": DiscountAmountCalculation(),
                        }
        data = {
            'requestData': requestData,
            "appId": "123456",
            "requestType": "1134",
            "dataSign": md5(data=requestData),
        }
        logger.info(data)
        headers = {
            "Content-Type": "applications/json",
            "language": "0"
        }
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.info(re.text)
        logger.info(re.headers)
    except Exception as e:
        print(e)

def Retreat():
    '''
    退劵(1135)
    :return:
    '''
    try:
        url = 'http://192.168.2.239:8767/gateway/exterfaceInvoke.json'
        requestData = {
            "couponNo": DiscountAmountCalculation(),
                        }
        data = {
            'requestData': requestData,
            "appId": "123456",
            "requestType": "1135",
            "dataSign": md5(data=requestData),
        }
        logger.info(data)
        headers = {
            "Content-Type": "applications/json",
            "language": "2"
        }
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.info(re.text)
        logger.info(re.headers)
    except Exception as e:
        print(e)
def DiscountAmountCalculation():
    '''
    接口四：优惠金额计算接口(1104)
    :return:
    '''
    try:
        url = 'http://192.168.2.239:8767/gateway/exterfaceInvoke.json'
        requestData = {
            "couponNo": DiscountAmountCalculation(),

                        }
        data = {
            'requestData': requestData,
            "appId": "123456",
            "requestType": "1135",
            "dataSign": md5(data=requestData),
        }
        logger.info(data)
        headers = {
            "Content-Type": "applications/json",
            "language": "2"
        }
        re = requests.post(url=url, data=json.dumps(data), headers=headers)
        logger.info(re.text)
        logger.info(re.headers)
    except Exception as e:
        print(e)

# SearchByNumber()
# DiscountAmountCalculation()
# CouponwriteoffStatistics()
# # Retreat()

if __name__ == '__main__':
    SearchByNumber()
    DiscountAmountCalculation()
    CouponwriteoffStatistics()
    Retreat()


