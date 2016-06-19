import socket, os, time
import subprocess
import chardet
import MySQLdb
import string
import datetime


  
address = ('127.0.0.1', 8000)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  



try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hackathon',db='freeswitch',port=3306)
    cur=conn.cursor()
    #for i in range(290001, 290001 + 8000):
        #cur.execute("insert into subscriber (username, domain, password) values (" + str(i) + ", '10.2.34.87', '1234')")
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

  
while True:  

    try:
        data, addr = s.recvfrom(2048)  

        if not data:  
            print "client has exist"  
            break  

        print "received:", data, "from", addr  

        time.sleep(2)

        datetime_m = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "datetime"
        print datetime_m


        #-----process all voice

        p =subprocess.Popen('ffmpeg -i /home/hackathon/source/hackathon/record/' + data + '.wav -f s16le -ar 8000 -acodec pcm_s16le /home/hackathon/source/hackathon/record/' + data + '.pcm', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        #baidu 

        try:
            cur.execute("set names utf8;") 
            str1 = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + data +".wav").read()
            print str1

            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'all', 'baidu', '" + str1 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()

            #yunzhiying
            p =subprocess.Popen('sample v2.hivoice.cn 80 /home/hackathon/source/hackathon/record/' + data + '.pcm ./result.txt', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            str1 = p.stderr.readline()
            print str1
            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'all', 'yunzhiying', '" + str1 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])







        #------process cdr 
        p =subprocess.Popen('/home/hackathon/source/hackathon/cdr/upload_cdr.pl', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()




        #------process in  voice
        p =subprocess.Popen('ffmpeg -f mulaw -ar 8000 -ac 1 -i /home/hackathon/source/hackathon/record/'+data+'-in.PCMU -ar 8000 -ac 1 /home/hackathon/source/hackathon/record/'+data+'-in.wav', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()

        time.sleep(2)

        p =subprocess.Popen('ffmpeg -i /home/hackathon/source/hackathon/record/' + data + '-in.wav -f s16le -ar 8000 -acodec pcm_s16le /home/hackathon/source/hackathon/record/' + data + '-in.pcm', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()


        try:
            #baidu
            str2 = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + data +"-in.wav").read()
            print str2
            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'in',  'baidu', '" + str2 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        try:
            #yunzhisheng
            p =subprocess.Popen('sample v2.hivoice.cn 80 /home/hackathon/source/hackathon/record/' + data + '-in.pcm ./result.txt', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            str1 = p.stderr.readline()
            print str1
            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'in', 'yunzhiying', '" + str1 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        

        #------process out  voice
        p =subprocess.Popen('ffmpeg -f mulaw -ar 8000 -ac 1 -i /home/hackathon/source/hackathon/record/' + data + '-out.PCMU -ar 8000 -ac 1 /home/hackathon/source/hackathon/record/' + data +'-out.wav', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()

        time.sleep(2)

        p =subprocess.Popen('ffmpeg -i /home/hackathon/source/hackathon/record/' + data + '-out.wav -f s16le -ar 8000 -acodec pcm_s16le /home/hackathon/source/hackathon/record/' + data + '-out.pcm', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()

                

        try:
            #baidu
            str3 = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + data +"-out.wav").read()
            print str3
            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'out', 'baidu', '" + str3 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

        try:
            #yunzhisheng
            p =subprocess.Popen('sample v2.hivoice.cn 80 /home/hackathon/source/hackathon/record/' + data + '-out.pcm ./result.txt', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            str1 = p.stderr.readline()
            print str1
            cur.execute("insert into voice_recognition (uuid, type, supplier, result, start_time) values ('" + data + "', 'out', 'yunzhiying', '" + str1 + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
            conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


        str1 = os.popen("python /home/hackathon/git/hackathon/wave/plot2.py " + data).read()
        str2 = os.popen("python /home/hackathon/git/hackathon/wave/plot2.py " + data + "-in").read()
        str3 = os.popen("python /home/hackathon/git/hackathon/wave/plot2.py " + data + "-out").read()
        print str1
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])



s.close() 
