from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wechatpy import parse_message
import hashlib

#公众号token
token = '123'

@csrf_exempt
def index(request):
    signature = request.GET['signature']
    echostr = request.GET['echostr']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    print("handle/GET func: hashcode, signature: ", hashcode, signature)
    if hashcode == signature:
        return HttpResponse(echostr)
    else:
        return ""
    xml = request.body.decode()
    msg = parse_message(xml)
    print(msg)
    # if msg.type == 'link':
    #     return HttpResponse()
    # else:
    #     return HttpResponse()
    return HttpResponse()
