import hashlib
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

# 公众号token
token = '123'


@csrf_exempt
def index(request):
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    list = [token, timestamp, nonce]
    logger.error(list)
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        xml = request.body.decode()
        msg = parse_message(xml)
        logger.error(msg)
        return HttpResponse()
    else:
        xml = request.body.decode()
        msg = parse_message(xml)
        logger.error(msg)
        return HttpResponse()

    # if msg.type == 'link':
    #     return HttpResponse()
    # else:
    #     return HttpResponse()
    return HttpResponse()
