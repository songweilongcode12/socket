import time, sched
import datetime

s = sched.scheduler(time.time, time.sleep)




# - * - encoding: utf - 8 -*-
import socket
import threading
import random
import json
import time
from loguru import logger
import time
import datetime
import logging
from locust import task,TaskSet,HttpLocust
from time import ctime
def GetMouth():
    '''
    生成随机的月份
    :return:
    '''
    mouth = random.randint(1,12)
    if mouth < 10:
        mouths = '0' + str(mouth)
    else:
        mouths = mouth
    # print('mouths:',mouths)
    return mouths
def OrderId():
    '''
    生成随机的唯一订单号
    :return:
    '''
    OrderNumber1 = random.randrange(135790,246810)
    # print('OrderNumber1:',OrderNumber1)
    OrderNumber2 = random.randrange(1357, 2468)
    # print('OrderNumber2:',OrderNumber2)
    Orderid = str(OrderNumber1) + '20191205' + str(OrderNumber2)
    return Orderid
def LocalData():
    '''
    获取本地时间
    :return:
    '''
    data_format = '%Y%m%d%H%M%S'
    locatTime = datetime.datetime.now().strftime(data_format)
    logger.info(locatTime)
    return locatTime
# LocalData()
def OrdinaryTransaction_amount():
    '''
    生成随机的交易金额
    :return:
    '''
    or_count = str(random.randrange(188,9000)) + str(random.randrange(8,89))
    logger.info(or_count)
    return or_count
def cloud_amount():
    '''
    生成随机的云闪付金额小于1000元
    :return:
    '''
    cl_count = str(random.randrange(1,999)) + str(random.randrange(8,98))
    logger.info(cl_count)
    return cl_count
# OrdinaryTransaction_amount()

def BaseMethod(cardState,tranAmt,OrderId,bTrans,tranDate):
    '''
    建立socket连接
    :return:
    '''
    # "merCode": "923000352518014"测试
    # "merCode": "847584053000050",正式
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # conn.connect(("183.57.43.214", 8999))
        conn.connect(("192.168.2.147", 8948))
        code1 = str.encode('eof')
        msg = {
                "merCode": "923000352518014",
                "merOrderId":OrderId,
                "tranAmt":tranAmt ,
                "tid":'96894778',
                # "tranDate": "2019"+str(GetMouth())+"03140526",
                "tranDate": tranDate,
                "md5Data": "B5E0A9E5",
                "acctNum": "166210946888170005 ",
                "revFlag": "0",
                "statAmt": "000000000000",
                "covDate": " ",
                "statRate": " ",
                "settDate": "20191209",
                "merType": "5411",
                "srvEntry": "072",
                "proFlag": "0",
                "resp": "00",
                "bTrans": bTrans,
                "cardState": cardState
                }
        data1 = str.encode(json.dumps(msg)) + code1
        length = str.encode(str(len(data1)))
        data2 = length + data1
        logger.info(data2)
        request_data = msg['merOrderId']
        conn.sendall(data2)
        # conn.close()
        responce_data = conn.recv(1026)
        # OrderNumber = str(responce_data)
        # print(OrderNumber.find('xxxxxxxx,',','))
        # logger.info(OrderNumber)
        logger.info(responce_data)
        if str(request_data) in str(responce_data):
            pass
        else:
            # logging.info(request_data)
            # print('responce_data:',responce_data)
            logging.ERROR('socket 丢包')
    except socket.timeout:
        logger.error('time out')
    except Exception as e:
        print('error:',e)
        return request_data
# def Transaction_Cancle(cardState,tranAmt,OrderId,bTrans):
#     BaseMethod(
#         cardState=cardState,
#         tranAmt=tranAmt,
#         OrderId=OrderId,
#         bTrans=bTrans,
#         tranDate=LocalData
#     )
class UserBehavior(TaskSet):

    def on_start(self):
        self.start_time = ctime()
        return self.start_time

    @task(weight=1)
    def CreditCardSecondsToTransactions(self):
        '''
        贷记卡秒到交易
        :return:
        '''
        BaseMethod(
            cardState='02101000',
            tranAmt=OrdinaryTransaction_amount(),
            OrderId=OrderId(),
            bTrans='PER',
            tranDate=LocalData
        )
        logger.info('贷记卡秒到交易')
        time.sleep(1)

    @task(weight=1)
    def CreditCardVIPTransactions(self):
        '''
        贷记卡VIP交易
        :return:
        '''
        BaseMethod(
            cardState='02101001',
            tranAmt=OrdinaryTransaction_amount(),
            OrderId=OrderId(),
            bTrans='PER'
        )
        logger.info('贷记卡VIP交易')
        # Transaction_Cancle(
        #     cardState='02101001',
        #     tranAmt=OrdinaryTransaction_amount(),
        #     OrderId=BaseMethod(),
        #     bTrans='PVR'
        # )
        time.sleep(1)
    @task(weight=1)
    def CloudflashTransaction(self):
        '''
        云闪付（小于1000）
        :return:
        '''
        BaseMethod(
            cardState='02101011',
            tranAmt=cloud_amount(),
            OrderId=OrderId(),
            bTrans='PER',
            tranDate=LocalData
        )
        logger.info('云闪付（小于1000）')
        time.sleep(1)
    @task(weight=1)
    def DebitCardSecondsToTransactions(self):
        '''
        借记卡秒到交易
        :return:
        '''
        BaseMethod(
            cardState='01101000',
            tranAmt=OrdinaryTransaction_amount(),
            OrderId=OrderId(),
            bTrans='PER',
            tranDate=LocalData
        )

        logger.info('借记卡秒到交易')
        time.sleep(1)

    def On_end(self):
        self.end_time = ctime()
        return self.end_time


class WebUserLocust(HttpLocust):
    weight = 1
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 5000
    # host = '183.57.43.214:8999'#product
    host = "192.168.2.147:8948"

# OrdinaryTransaction_amount()
# BaseMethod(cardState='02101000',
#            tranAmt=OrdinaryTransaction_amount(),
#            OrderId=OrderId(),
#            bTrans='PER',
#            tranDate=LocalData()
#            )
# logger.info('贷记卡秒到交易')
#
# BaseMethod(cardState='02101001',
#            tranAmt=OrdinaryTransaction_amount(),
#            OrderId=OrderId(),
#            bTrans='PER',
#            tranDate=LocalData()
#            )
# logger.info('贷记卡VIP交易')
# BaseMethod(cardState='02101011',
#            tranAmt='100000',
#            OrderId=OrderId(),
#            bTrans='PER',
#            tranDate=LocalData()
#             )
# logger.info('云闪付交易')
# BaseMethod(cardState='01101000',
#            tranAmt=OrdinaryTransaction_amount(),
#            OrderId=OrderId(),
#            bTrans='PER',tranDate=LocalData()
#            )
# logger.info('借记卡秒到交易')
# BaseMethod(cardState='01101001',
#            tranAmt=OrdinaryTransaction_amount(),
#            OrderId=OrderId(),
#            bTrans='PER',tranDate=LocalData()
#            )
# logger.info('借记卡秒到交易')



def event_fun1():
    print("func1 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    BaseMethod(cardState='01101001',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER', tranDate=LocalData()
               )
    logger.info('借记卡秒到交易')
    BaseMethod(cardState='01101000',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER', tranDate=LocalData()
               )
    logger.info('借记卡秒到交易')
    BaseMethod(cardState='02101011',
               tranAmt='100000',
               OrderId=OrderId(),
               bTrans='PER',
               tranDate=LocalData()
               )
    logger.info('云闪付交易')
    BaseMethod(cardState='02101000',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER',
               tranDate=LocalData()
               )
    logger.info('贷记卡秒到交易')

    BaseMethod(cardState='02101001',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER',
               tranDate=LocalData()
               )
    logger.info('贷记卡VIP交易')

def perform1(inc):
    s.enter(inc, 0, perform1, (inc,))
    event_fun1()


def event_fun2():
    print("func2 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    BaseMethod(cardState='02101000',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER',
               tranDate=LocalData()
               )
    logger.info('贷记卡秒到交易')

    BaseMethod(cardState='02101001',
               tranAmt=OrdinaryTransaction_amount(),
               OrderId=OrderId(),
               bTrans='PER',
               tranDate=LocalData()
               )
    logger.info('贷记卡VIP交易')


def perform2(inc):
    s.enter(inc, 0, perform2, (inc,))
    event_fun2()


def mymain(func, inc=2):
    if func == "1":
        s.enter(0, 0, perform1, (0.001,))# 每隔10秒执行一次perform1
    # if func == "2":
    #     s.enter(0, 0, perform2, (0.01,))# 每隔20秒执行一次perform2
if __name__ == '__main__':
    mymain('1')
    # mymain('2')
    s.run()