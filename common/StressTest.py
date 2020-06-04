from locust import TaskSet, task, HttpLocust
import queue
import json
import time
import logging
import random
import socket
log = logging.getLogger(__name__)

# 2018-11-23 21:05:..:... 精确到毫秒
twepoch = 1542978345588

worker_id_bits = 5
data_center_id_bits = 5
max_worker_id = -1 ^ (-1 << worker_id_bits)
max_data_center_id = -1 ^ (-1 << data_center_id_bits)
sequence_bits = 12
worker_id_shift = sequence_bits
data_center_id_shift = sequence_bits + worker_id_bits
timestamp_left_shift = sequence_bits + worker_id_bits + data_center_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)
def snowflake_to_timestamp(_id):
    _id = _id >> 22  # strip the lower 22 bits
    _id += twepoch  # adjust for twitter epoch
    _id = _id / 1000  # convert from milliseconds to seconds
    return _id


def generator(worker_id, data_center_id, sleep=lambda x: time.sleep(x / 1000.0)):
    assert 0 <= worker_id <= max_worker_id
    assert 0 <= data_center_id <= max_data_center_id

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time() * 1000)

        if last_timestamp > timestamp:
            log.warning(
                "clock is moving backwards. waiting until %i" % last_timestamp)
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                log.warning("sequence overrun")
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp
        yield (((timestamp - twepoch) << timestamp_left_shift) |
               (data_center_id << data_center_id_shift) |
               (worker_id << worker_id_shift) |
               sequence)

s = generator(1, 1)
# print(s)
for i in range(1):
    orderid = s.__next__()
    print("orderid:",orderid)

class UserBehavior(TaskSet):
    @task
    def test_register(self):
        try:
            # get_nowait() 取不到数据直接崩溃；get() 取不到数据会一直等待
            data = self.locust.user_data_queue.get_nowait()  # 取值顺序 'username': 'test0000'、'username': 'test0001'、'username': 'test0002'...
        except queue.Empty:  # 取不到数据时，走这里
            print('account data run out, test ended.')
            exit(0)
        print('register with user: {}, pwd: {}'.format(data['merOrderId'], data['tranDate']))
        body = {
            "merCode": "923000352518014",
            "merOrderId": data['merOrderId'],
            "tranAmt": "500000",
            "tid": None,
            "tranDate": data['tranDate'],
            "md5Data": "B5E0A9E5",
            "acctNum": "166210946888170005 ",
            "revFlag": "0",
            "statAmt": "000000000000",
            "covDate": " ",
            "statRate": " ",
            "settDate": "20191202",
            "merType": "5411",
            "srvEntry": "072",
            "proFlag": "0",
            "resp": "00",
            "bTrans": "PER",
            "cardState": "0210101"
        }
        data1 = str.encode(json.dumps(body)) + str.encode('eof')
        length = str.encode(str(len(data1)))
        data2 = length + data1
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.sendall(data2)

        # conn.close()
        responce_data = conn.recv(1026)
        print(responce_data)
        # r = self.client.post('/user/signin', data=body).text
        # assert r.status_code == 200


class WebsiteUser(HttpLocust):
    host = '192.168.2.147:8948'
    task_set = UserBehavior
    user_data_queue = queue.Queue()  # 创建队列，先进先出
    for index in range(1):
        # data = {
        #     "username": "test%04d" % index,
        #     "password": "pwd%04d" % index,
        #     "email": "test%04d@debugtalk.test" % index,
        #     "phone": "186%08d" % index,
        # }
        # code1 = str.encode('eof')
        mouth = random.randint(1, 12)
        if mouth < 10:
            mouths = '0' + str(mouth)
        else:
            mouths = mouth
        print('mouths:', mouths)
        msg = {
            "merCode": "923000352518014",
            "merOrderId": orderid,
            "tranAmt": "500000",
            "tid": None,
            "tranDate": "2019" + str(mouths) + "03140526",
            "md5Data": "B5E0A9E5",
            "acctNum": "166210946888170005 ",
            "revFlag": "0",
            "statAmt": "000000000000",
            "covDate": " ",
            "statRate": " ",
            "settDate": "20191202",
            "merType": "5411",
            "srvEntry": "072",
            "proFlag": "0",
            "resp": "00",
            "bTrans": "PER",
            "cardState": "0210101"
        }
        # data1 = str.encode(json.dumps(msg)) + code1
        # length = str.encode(str(len(data1)))
        # data2 = length + data1
        user_data_queue.put_nowait(msg)  # 循环加入队列<全部>,循环完，继续执行
        print(user_data_queue)
    min_wait = 1000
    max_wait = 3000



