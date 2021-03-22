# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 12:03:56 2020

@author: 李运辰
"""
import requests
import time
from lxml import etree
import os
import json
#from flask_cors import CORS
from flask import Flask,render_template,request,Response,redirect,url_for
#内网ip
app = Flask(__name__)
###此处改为自己的ip地址，在index.html中两次也记得更改
ip="127.0.0.1"


headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
        }


###获取信息
def getlist(name_i):
    url_name = "https://baike.baidu.com/search/word?word="+str(name_i)
    s = requests.Session()
    response = s.get(url_name, headers=headers)
    text = response.text
    t_split = text.split('id="J-vars" data-lemmaid="')[1].split('" data-lemmatitle="')[0]
    #print(t_split)


    url="https://baike.baidu.com/item/"+str(name_i)+"/"+str(t_split)+"?fr=aladdin"
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    text = res.text


    selector = etree.HTML(text)
    #属性
    key = []
    #值
    value = []

    dt =[]
    dd =[]
    basicInfo_left = selector.xpath('//*[@class="basicInfo-block basicInfo-left"]')[0]
    dt.append(basicInfo_left.xpath('.//dt'))
    dd.append(basicInfo_left.xpath('.//dd'))

    basicInfo_right = selector.xpath('//*[@class="basicInfo-block basicInfo-right"]')[0]
    dt.append(basicInfo_right.xpath('.//dt'))
    dd.append(basicInfo_right.xpath('.//dd'))


    for j in dt:
        for i in j:
            text = i.xpath('.//text()')
            if len(text)==1:
                text = text[0].replace(" ","").replace("\n","").replace("\xa0","")
            else:
                text = "-".join(text)
                text = text.replace(" ", "").replace("\n", "").replace("\xa0", "")
            key.append(text)
    for j in dd:
        for i in j:
            text = i.xpath('.//text()')
            if len(text) == 1:
                text = text[0].replace(" ", "").replace("\n", "").replace("\xa0", "")
            else:
                text = "-".join(text)
                text = text.replace(" ", "").replace("\n", "").replace("\xa0", "").replace("-", " ")
            value.append(text)

    links=[]

    for k in range(0,len(key)):
        if key[k]=="代表作品"  or key[k]=="主要成就":
            v = value[k].split(" ")
            dict = {'source': str(name_i), 'target': str(v[0]+v[1]), 'rela': str(key[k]), 'type': 'resolved'}
            links.append(dict)
        else:
            dict= {'source': str(name_i), 'target': str(value[k]), 'rela': str(key[k]), 'type': 'resolved'}
            links.append(dict)

    return links

############################flask路由
#进入首页
@app.route('/')
def index():
    return render_template('index.html')
#获取数据
@app.route('/getdata')
def getdata():
    name_i = request.args.get('name')
    # 采集数据
    links = getlist(name_i)

    #return Response(json.dumps(links), mimetype='application/json')
    return render_template('index.html', linkss=json.dumps(links))

      
if __name__ == "__main__":    
    """初始化"""

    app.run(host=''+ip, port=5000,threaded=True)

