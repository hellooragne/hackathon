#encoding=utf-8

import wave
import sys
import urllib, urllib2, pycurl
import base64
import json

import binascii
## get access token by api key & secret key



def get_token():

    apiKey = "NRRZT6vY7FH6GASbdKydpF31"
    secretKey = "ctQXyz9049rdfTYPbMKIT1Sq908yzIhr"

    #print apiKey

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    #print auth_url

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']

def dump_res(buf):

    try:
        print buf
        #print json.loads(buf)['result'][1]
    except:
        pass

"""
    res = json.loads(buf)

    if 'result' in res.keys():
        print json.loads(buf)['result'][0]
"""

## post audio to server
def use_cloud(token, file_path):
    #print token
    #fp = wave.open('4.wav', 'rb')
    fp = wave.open(file_path, 'rb')
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    #print f_len, len(audio_data)

    #output = binascii.hexlify(audio_data)
    #print(output)

    cuid = "5298059" #my xiaomi phone MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=8000',
        'Content-Length: %d' % f_len
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val

if __name__ == "__main__":
    token = get_token()
    #print sys.argv[1]
    use_cloud(token,sys.argv[1])
