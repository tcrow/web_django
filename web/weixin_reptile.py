# # coding:utf-8
import http.cookiejar
import json
import time
from urllib import request
from . import view

import requests

cookie = http.cookiejar.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
handler = request.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = request.build_opener(handler)  # 通过handler来构建opener
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Host': 'mp.weixin.qq.com',
    'Connection': 'keep-alive',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': ' 1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Cookie': '',
}


def __save_es(item, prefix):
    if 'app_msg_ext_info' not in item:
        return
    comm = item['comm_msg_info']
    info = item['app_msg_ext_info']
    title = info['title']
    content_url = info['content_url']
    content_url = content_url.replace('\/', '/')
    if len(content_url.strip()) == 0:
        return
    try:
        print(content_url)
        page = request.urlopen(content_url)
    except Exception as e:
        print("访问微信链接出错了，错误原因" + e)
        return
    content = page.read().decode("utf-8")
    __post_es(prefix + ' ' + title, content_url, content, comm['datetime'])


'''
推送文章数据给搜索引擎
'''


def __post_es(name, source_url, content, datetime):
    h = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    params = {
        "name": name,
        "source_url": source_url,
        "content": content,
        "datetime": datetime
    }
    resp = requests.post(view.es_url + view.index, headers=h, data=json.dumps(params))
    print(resp.content)


def reptile(url, prefix):
    r = request.Request(url=url, headers=headers, method="GET")
    response = opener.open(r)
    offset = url[url.index('offset='):]
    offset = int(offset[7:offset.index('&')])
    htmlcode = response.read().decode()
    j = json.loads(htmlcode)
    if j['ret'] != 0:
        print('返回数据错误，请检查链接')
        exit(0)
    next_offset = j['next_offset']
    if offset == next_offset:
        return
    general_msg_list = j['general_msg_list']
    general_msg_list = json.loads(general_msg_list)
    for item in general_msg_list['list']:
        __save_es(item, prefix)
    # 非常重要，为了防止被封，每次抓取数据需要休息15秒
    time.sleep(15)
    reptile(url.replace("offset=" + str(offset), 'offset=' + str(next_offset)), prefix)
