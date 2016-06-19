import socket, os, time
import subprocess
import chardet
import MySQLdb
import string
import datetime
import thread


  
address = ('127.0.0.1', 9001)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  



try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hackathon',db='freeswitch',port=3306)
    cur=conn.cursor()
    #for i in range(290001, 290001 + 8000):
        #cur.execute("insert into subscriber (username, domain, password) values (" + str(i) + ", '10.2.34.87', '1234')")
except MySQLdb.Error,e:

     print "Mysql Error %d: %s" % (e.args[0], e.args[1])



def real_time_domain():
    address = ('127.0.0.1', 9000)  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    s.bind(address)

    while True:
        data, addr = s.recvfrom(2048)  

        print "received:", data, "from", addr 
        
        global uuid
        uuid = data
 
        global rtp_num
        rtp_num = 0
       
    
    s.close() 


thread.start_new_thread(real_time_domain, ())


  
while True:  

    try:
        data, addr = s.recvfrom(2048)  

        if not data:  
            print "client has exist"  
            break  

        #print "received:", data, "from", addr  
        
        global uuid
        global rtp_num


        if uuid == "":
            continue  
        
        if rtp_num < 3:
            rtp_num = rtp_num + 1
            continue
        else:
            rtp_num = 0
            print "rtp_num over"

        datetime_m = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #------process in  voice
        p =subprocess.Popen('ffmpeg -y -f mulaw -ar 8000 -ac 1 -i /home/hackathon/source/hackathon/record/'+uuid+'-in.PCMU -ar 8000 -ac 1 /home/hackathon/source/hackathon/record/'+uuid+'-in.wav', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()



        try:
            #baidu
            #print "python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + uuid +"-in.wav"
            str2 = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + uuid +"-in.wav").read()
            print str2
            #cur.execute("insert into voice_real_time (uuid, type, supplier, result, start_time) values ('" + uuid + "', 'in',  'baidu', '" + str2 + "', " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")")
            #conn.commit()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])




        #------process out  voice
        p =subprocess.Popen('ffmpeg -y -f mulaw -ar 8000 -ac 1 -i /home/hackathon/source/hackathon/record/' + uuid + '-out.PCMU -ar 8000 -ac 1 /home/hackathon/source/hackathon/record/' + uuid +'-out.wav', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        #print p.stderr.readline()



        try:
            #baidu
            str3 = os.popen("python /home/hackathon/source/hackathon/recognition/baidu.py  /home/hackathon/source/hackathon/record/" + uuid +"-out.wav").read()
            print str3
            #cur.execute("insert into voice_real_time (uuid, type, supplier, result, start_time) values ('" + uuid + "', 'out', 'baidu', '" + str3 + "', " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ")")
            #conn.commit()
        except Exception , e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


    except Exception , e:
        print e 


s.close() 
