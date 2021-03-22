# -*- coding: utf-8 -*-


"""
李运辰 2021-3-21

公众号：python爬虫数据分析挖掘
"""


import requests
from lxml import etree
import json
import time
headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36',
        }


###获取每一页的商品数据
def getlist():

    url="https://baike.baidu.com/item/刘德华/114923?fr=aladdin"
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
        dict= {'source': '刘德华', 'target': str(key[k]), 'rela': str(value[k]), 'type': 'resolved'}
        links.append(dict)
        #print(key[k]+":"+value[k])
    print(links)


    """
    var
    links =
    [
        {source: '艾伦·麦席森·图灵', target: 'Alan Mathison Turing', 'rela': '外文名', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '英国', 'rela': '国籍', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '英国伦敦', 'rela': '出生地', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '1912年6月23日', 'rela': '出生日期', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '1954年6月7日', 'rela': '逝世日期', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '数学家，逻辑学家，密码学家', 'rela': '职业', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '剑桥大学国王学院，普林斯顿大学', 'rela': '毕业院校', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '“计算机科学之父”', 'rela': '主要成就', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '提出“图灵测试”概念', 'rela': '主要成就', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '人工智能', 'rela': '主要成就', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '破解德国的著名密码系统Enigma', 'rela': '主要成就', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '《论数字计算在决断难题中的应用》', 'rela': '代表作品', type: 'resolved'},
        {source: '艾伦·麦席森·图灵', target: '《机器能思考吗？》', 'rela': '代表作品', type: 'resolved'},
    ];
    """



url="https://baike.baidu.com/search/word?word=刘德华"
s = requests.Session()
response = s.get(url, headers=headers)
text = response.text
t_split = text.split('id="J-vars" data-lemmaid="')[1].split('" data-lemmatitle="')[0]
print(text)
getlist()





