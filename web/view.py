import json

import requests
from django.shortcuts import render
from django.http import HttpResponse

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['user'] = 'TCrow'
    return render(request, 'hello.html', context)


def show(request):
    url = "http://127.0.0.1:9200/meituan/blog/" + request.GET['id']
    r = requests.get(url)
    return HttpResponse(json.loads(r.content)["_source"]["content"])


def search(request):
    url = "http://127.0.0.1:9200/meituan/blog/_search"
    data = {
        "query": {
            "match": {
                "name": request.GET['q']
            }
        },
        "size": 10
    }
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers, data=json.dumps(data))
    hits = json.loads(r.content)['hits']['hits']
    list = []
    for item in hits:
        blog = item['_source']
        blog['id'] = item['_id']
        list.append(blog)
    context = {}
    context['list'] = list
    return render(request, 'list.html', context)
