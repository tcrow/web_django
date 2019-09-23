import json

import requests
from django.http import HttpResponse
from django.shortcuts import render

es_url = 'http://10.0.0.39:9200'
index = '/meituan/blog'


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['user'] = 'TCrow'
    return render(request, 'hello.html', context)


def show(request):
    url = es_url + index + '/' + request.GET['id']
    r = requests.get(url)
    return HttpResponse(json.loads(r.content)["_source"]["content"])


def search(request):
    url = es_url + index + "/_search"
    must = []
    if len(request.GET['q'].strip()):
        must.append({
            "match": {
                "name": request.GET['q']
            }
        })
    if len(request.GET['c'].strip()):
        must.append({
            "match_phrase": {
                "content": request.GET['c']
            }
        })
    start = int(request.GET['p']) * 10
    data = {
        "size": 10,
        "from": start,
        "sort": [
            {
                "datetime": {
                    "order": "desc"
                }
            }
        ],
        "query": {
            "bool": {
                "must": must
            }
        }
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
    context['c'] = request.GET['c']
    context['q'] = request.GET['q']
    context['p'] = request.GET['p']

    return render(request, 'list.html', context)
