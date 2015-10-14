"""lets find how fork work in python """ 

import os
def child():
    print 'a new child', os.getpid()
    os._exit(0)

def parent():
    while True:
        new  = os.fork()
        if new == 0:  # we are in child
	    child()
	else:
	    pids = (os.getpid(), new)
	    print 'parent:%d, child:%d' % pids
	if raw_input() == 'q':
	    break

parent()
