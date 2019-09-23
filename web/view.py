import json

import requests
from django.shortcuts import render
from django.http import HttpResponse

es_url = 'http://127.0.0.1:9200'
index = '/meituan/blog/'

def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['user'] = 'TCrow'
    return render(request, 'hello.html', context)


def show(request):
    url = es_url + index + request.GET['id']
    r = requests.get(url)
    return HttpResponse(json.loads(r.content)["_source"]["content"])


def search(request):
    url = es_url + index + "/_search"
    data = {
        "query": {
            "match": {
                "name": request.GET['q']
            },
            "match_phrase": {
                "content": request.GET['c']
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
