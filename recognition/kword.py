# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests
import sys


KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'


#text = '病毒式媒体网站：让新闻迅速蔓延'

text = sys.argv[1] 
params = {'top_k': 10}
data = json.dumps(text)
headers = {'X-Token': 'e1GrPn7V.8343.U_qDn-ZaRQiq'}
resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))


for weight, word in resp.json():
    print(weight, word)



SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis'
# 注意：在测试时请更换为您的API Token
headers = {'X-Token': 'e1GrPn7V.8343.U_qDn-ZaRQiq'}

s = ['他是个傻逼', '美好的世界']
data = json.dumps(s)
resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))

print(resp.text)
