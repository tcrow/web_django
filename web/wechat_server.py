from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from wechatpy import parse_message


@csrf_exempt
def index(request):
    xml = request.body.decode()
    msg = parse_message(xml)
    print(msg)
    # if msg.type == 'link':
    #     return HttpResponse()
    # else:
    #     return HttpResponse()
    return HttpResponse()
