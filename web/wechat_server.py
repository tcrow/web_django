import hashlib
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message
import threading

from . import weixin_reptile

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)

# 公众号token
token = '123'
lock = threading.RLock()


@csrf_exempt
def index(request):
    logger.error('一个请求过来了')
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    if hashcode == signature:
        parse(request)
    else:
        parse(request)

    return HttpResponse()

def parse(request):
    xml = request.body.decode()
    msg = parse_message(xml)
    logger.error(msg)
    content = msg.content
    if msg.type == 'text' and 'https://mp.weixin.qq.com/mp/profile_ext?action=home' in content:
        logger.error(content)
        flag = lock.acquire(timeout=3)
        if flag:
            try:
                weixin_reptile.reptile(content,None)
            finally:
                lock.release()
        else:
            return HttpResponse('正在执行中，请稍后重试')
        return HttpResponse()
    else:
        return HttpResponse()