import os, sys, time
from freeswitch import *

# everything after the command (in this case pyrun) and
# the module name (in this case foo.postprocessing) will
# be interpreted as a string and handed to our 'runtime'
# function where it will be accessible via the argument 'arg1'

def handler(session, args):
    consoleLog( "info", "Caller: %s hung up 10s ago!\n")
    pass

def fsapi(session, stream, env, args):
    consoleLog( "info", "Caller: %s hung up 10s ago 222!\n")
    str = os.popen("sh /home/hackathon/source/hackathon/run.sh").read()
    consoleLog( "info", str)
    pass

if __name__ == "__main__":
    while True:
	str = os.popen("sh /home/hackathon/source/hackathon/run.sh").read()
    	consoleLog( "info", str)	
	time.sleep(5)
