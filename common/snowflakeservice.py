import time
import logging
from loguru import logger
import time
import datetime
def Timestamp():
    dtime = datetime.datetime.now()
    un_time = time.mktime(dtime.timetuple())
    # 将unix时间戳转换为“当前时间”格式
    times = datetime.datetime.fromtimestamp(un_time)
    logger.debug(times)
    return time

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
    _id += Timestamp  # adjust for twitter epoch
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
            logger.warning(
                "clock is moving backwards. waiting until %i" % last_timestamp)
            sleep(last_timestamp - timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                logger.warning("sequence overrun")
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp
        yield (((timestamp - Timestamp) << timestamp_left_shift) |
               (data_center_id << data_center_id_shift) |
               (worker_id << worker_id_shift) |
               sequence)


if __name__ == '__main__':
    s = generator(1,1)
    print(s)
    for i in range(1):
        orderid = s.__next__()
        print(orderid)
        # print(s.__next__())



