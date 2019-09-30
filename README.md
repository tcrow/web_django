# 爬取公众号文章和利用ElasticSearch搜索的功能演示


项目展示了如何利用ElasticSearch保存并搜索微信公众号的文章  
项目访问路径说明  
ctx + / 项目首页提供文章搜索功能  
ctx + /reptile/ 爬虫首页
ctx + /wechat/ 微信消息接口    

# 使用方法：  
```
pip install django
pip install wechatpy
pip install wechatpy[cryptography]
python manage.py runserver
```

# 路线图计划：    
- [x] 实现微信公众号自动解析读取功能
- [x] 实现微信公众号文章搜索功能
- [ ] 实现公众号消息接口，转发公众号主页给设置的公众号后，自动解析读取公众号文章，实现文章搜索，不再需要手工提交公众号URL
- [ ] 界面及交互优化


==警告，这只是一个Demo，仅用于技术研究和学习，用于生产环境造成的任何后果和法律责任本人概不负责==