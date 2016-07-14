# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests
import sys

import wave
import sys
import socket, os, time
import subprocess
import chardet
import MySQLdb
import string
import datetime
import json


KEYWORDS_URL = 'http://api.bosonnlp.com/keywords/analysis'


#text = '病毒式媒体网站：让新闻迅速蔓延'

text = sys.argv[1] 

"""
params = {'top_k': 10}
data = json.dumps(text)
headers = {'X-Token': 'e1GrPn7V.8343.U_qDn-ZaRQiq'}
resp = requests.post(KEYWORDS_URL, headers=headers, params=params, data=data.encode('utf-8'))


for weight, word in resp.json():
    print(weight, word)
"""


SENTIMENT_URL = 'http://api.bosonnlp.com/sentiment/analysis?weibo'
# 注意：在测试时请更换为您的API Token
headers = {'X-Token': 'AXwGot59.8387.Pt9Okk3G0B0Y'}

s = [sys.argv[4]]
data = json.dumps(s)
resp = requests.post(SENTIMENT_URL, headers=headers, data=data.encode('utf-8'))

print(resp.text)

try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hackathon',db='freeswitch',port=3306)
    cur=conn.cursor()
    #for i in range(290001, 290001 + 8000):
        #cur.execute("insert into subscriber (username, domain, password) values (" + str(i) + ", '10.2.34.87', '1234')")
except MySQLdb.Error, e:
    #print  e.args[1]
    pass

cur.execute("insert into voice_kword (uuid, type, supplier , emotion , start_time) values ('" + sys.argv[1] + "', '" + sys.argv[2]+ "',  '" + sys.argv[3] + "','" + resp.text + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")

conn.commit()
