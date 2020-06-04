import hashlib
import string
import random
import json
from loguru import logger
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

# def md5hex(word):
#     """ MD5加密算法，返回32位小写16进制符号 """
#     if isinstance(word, unicode):
#         word = word.encode("utf-8")
#     elif not isinstance(word, str):
#         word = str(word)
#     m = hashlib.md5()
#     m.update(word)
#     return m.hexdigest()
import json
import decimal

data = {'key1': 'string', 'key2': 10, 'key3': decimal.Decimal('1.45')}
class DecimalEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, decimal.Decimal):
             return float(obj)
         return super(DecimalEncoder, self).default(obj)

print(json.dumps(data, cls=DecimalEncoder))
