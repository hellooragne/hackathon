import wave
import sys
import socket, os, time
import subprocess
import chardet
import MySQLdb
import string
import datetime
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
#import pylab as pl
import matplotlib.pyplot as pl

# ============ test the algorithm =============
# read wave file and get parameters.

filename = sys.argv[1]
print "/home/hackathon/source/hackathon/record/" + filename + ".wav"
fw = wave.open("/home/hackathon/source/hackathon/record/" + filename + ".wav",'rb')
params = fw.getparams()
print(params)
nchannels, sampwidth, framerate, nframes = params[:4]
strData = fw.readframes(nframes)
waveData = np.fromstring(strData, dtype=np.int16)
#waveData = waveData*1.0/max(abs(waveData))  # normalization
waveData = waveData*1.0  # normalization

soundInfo = np.fromstring(strData,np.int16)
f = fw.getframerate()

fw.close()


# plot the wave
time = np.arange(0, len(waveData)) * (1.0 / framerate)

index1 = 10000.0 / framerate
index2 = 10512.0 / framerate
index3 = 15000.0 / framerate
index4 = 15512.0 / framerate

gate = 1000
continue_num = 8000

start_num = 0
end_num = 0
continue_flag = 0

wave_result = []

print "waveDate len:", len(waveData)
for index in range(len(waveData)):
    if waveData[index] < gate:
        if continue_flag == 0:
            start_num = index 
            continue_flag = 1
    else:
        if (index - start_num) > continue_num and continue_flag == 1:
           #print "start num", start_num , "end num", index, "start_time:", start_num * (1.0 / framerate), "end time:", index * (1.0 / framerate)
           wave_result.append("start num:" + str(start_num) + " end num:" + str(index) + " start_time:"+ str(start_num * (1.0 / framerate))+ " end time:"+ str(index * (1.0 / framerate)) + "\n")
        continue_flag = 0

    if index + 1 == len(waveData):
        #print "end:", index, "start num", start_num, "continue_flag", continue_flag
        if (index - start_num) > continue_num and continue_flag == 1:
           #print "start num", start_num , "end num", index, "start_time:", start_num * (1.0 / framerate), "end time:", index * (1.0 / framerate)
           wave_result.append("start num" + str(start_num) + " end num" + str(index) + " start_time:"+ str(start_num * (1.0 / framerate))+ " end time:"+ str(index * (1.0 / framerate)) + "\n")
print ''.join(wave_result)


try:
    conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='hackathon',db='freeswitch',port=3306)
    cur=conn.cursor()
    #for i in range(290001, 290001 + 8000):
        #cur.execute("insert into subscriber (username, domain, password) values (" + str(i) + ", '10.2.34.87', '1234')")
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

cur.execute("insert into voice_wave (uuid, type,  result, pic, start_time) values ('" + filename + "', 'in',  '" + ''.join(wave_result) + "','" + filename + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
conn.commit()





pl.subplot(211)
pl.plot(time, waveData)
pl.plot([index1,index1],[-1,1],'r')
pl.plot([index2,index2],[-1,1],'r')
pl.plot([index3,index3],[-1,1],'g')
pl.plot([index4,index4],[-1,1],'g')
pl.xlabel("time (seconds)")
pl.ylabel("Amplitude")

#pl.subplot(312)
#pl.plot(np.arange(512),waveData[10000:10512],'r')
#pl.plot([59,59],[-1,1],'b')
#pl.plot([169,169],[-1,1],'b')
#print(1/( (169-59)*1.0/framerate ))
#pl.xlabel("index in 1 frame")
#pl.ylabel("Amplitude")

#pl.subplot(313)
#pl.plot(np.arange(512),waveData[15000:15512],'g')
#pl.xlabel("index in 1 frame")
#pl.ylabel("Amplitude")

pl.subplot(212)
pl.specgram(soundInfo,Fs = f, scale_by_freq = True, sides = 'default')
pl.ylabel('Frequency')
pl.xlabel('time(seconds)')
pl.savefig("/home/hackathon/source/hackathon/pic/" + sys.argv[1] + ".png")
#pl.show()
