'''************************************************************************** 
RC car control GUI
Sends python GEt requests to control the car

pass commands like: 
http://x.x.x.x/set?p0=1&p2=1&duration=1000 => 2 buttons pressed for 1s
http://x.x.x.x/set?p0=1&duration=500 => 1 button pressed for 0.5s

or (using DNS)
http://esprccar.local/set?p0=1&duration=500

Author: fvilmos, https://github.com/fvilmos
***************************************************************************'''

# resources:
# https://skillshats.com/blogs/send-http-requests-as-fast-as-possible-in-python/


import cv2
import numpy as np
import sys
import requests

from threading import Thread,local
from queue import Queue

# slider definition
slider_max = 2000
duration = 100
last_key = 0
gui_name="WiFi RC car control GUI"

# creates an empty image
window = np.zeros(shape=[240,320,3])

url = 'http://esprccar/set?'
http_response = ''

# delay for the key repetition
reset_threshold = 2
activate = True

# windows to hold the trackbar
cv2.namedWindow(gui_name)

queue = Queue(maxsize=1)

# thread with local storage
thread_local = local() 

# theread worker
def worker():
    '''
    send requests using the session object, if queue is not empty
    '''
    global activate
    # create a session object if not exists
    if not hasattr(thread_local,'session'):
        thread_local.session = requests.Session()
    session = thread_local.session

    # consume url
    while True:
        if not queue.empty():
            url = queue.get()
            try:
                session.get(url)
            except:
                print ("No connection to the Wifi board!")
                session.close()
                activate = False
                

# create worker thread
worker_thread = Thread(target=worker, daemon=True)
worker_thread.start()

# slider handler
def on_trackbar(val):
    global duration
    duration = val

# trackbar
cv2.createTrackbar('duration', gui_name , 0, slider_max, on_trackbar)

def drwaw_keys(img,p_index=0,symbolic=''):
    '''
    helper to draw the GUI buttons, colors on red when pressed
    '''
    global last_key
    if p_index is not None:
        last_key=p_index

    position = [(70,30,50,30),(130,30,50,30),(190,30,50,30),(130,80,50,30),(70,80,50,30),(190,80,50,30)]

    for i,val in enumerate(position):
        if last_key == 0:
            cv2.rectangle(img,val,[0,255,0],-1)
        else:
            if last_key == i+1:
                cv2.rectangle(img,val,[0,0,255],-1)
            else:
                cv2.rectangle(img,val,[0,255,0],-1)
    
    # desplay simbolic name
    if symbolic !="":
        cv2.putText(img, "pressed: " + str(symbolic), [10,20], cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255,255,255], 1, cv2.LINE_AA)

def cmd_api(set_port_string="0001", skipp_zeros=False):
    '''
    send commands to RC car using a string format
    if skipp_zeros = True, values will be sent without zeros.
        ex. cmd_api(set_port_string="0001", skipp_zeros=False) -> http://esprccar/set?p0=1&p1=0&p2=0&p3=0
            cmd_api(set_port_string="0001", skipp_zeros=True) -> http://esprccar/set?p0=1
    if 'x' is uesd in the string, the respective ports are ignored.
        ex. cmd_api(set_port_string="x0x1", skipp_zeros=False) -> http://esprccar/set?p0=1&p2=0
    '''
    ltemp = list(set_port_string)
    lcmd = []
    for i in range(len(ltemp)):
        if skipp_zeros==False:
            if ltemp[len(ltemp)-i-1] != "x":
                lcmd.append("p"+str(i)+"="+ltemp[len(ltemp)-i-1])
        else:
            if ltemp[len(ltemp)-i-1] == "1":
                lcmd.append("p"+str(i)+"="+ltemp[len(ltemp)-i-1])


    #create cmd string
    cmd = ''
    for c in lcmd:
        cmd +="&"+c
    
    # skipp first character
    cmd = cmd[1:]

    #send commad
    queue.put(url+cmd)

def main():
    '''
    handle gui related information
    '''
    #global activate
    neg_ports = 0
    count = 0
    while activate:
        window = np.zeros(shape=[240,320,3])
        cv2.putText(window, 'press keys: q,w,e,a,s,d', [10,10], cv2.FONT_HERSHEY_SIMPLEX, 0.4, [255,255,255], 1, cv2.LINE_AA)

        # read keys
        k = cv2.waitKey(100)

        # escape
        if k == 27:
            sys.exit(0)

        # forward
        if k == ord('w'):
            cmd_api("xxx1",skipp_zeros=False)
            drwaw_keys(window, 2,'w')
            neg_ports = 1

        # back
        elif k == ord('s'):
            cmd_api("xx1x",skipp_zeros=False)
            drwaw_keys(window, 4,'s')
            neg_ports = 2
        
        # left
        elif k == ord('a'):
            cmd_api("x1xx",skipp_zeros=False)
            drwaw_keys(window, 5, 'a')
            neg_ports = 4
        
        # right
        elif k == ord('d'):
            cmd_api("1xxx",skipp_zeros=False)
            drwaw_keys(window, 6, 'd')
            neg_ports = 8

        # forward & right
        elif k == ord('e'):
            cmd_api("1xx1",skipp_zeros=False)
            drwaw_keys(window, 3, 'e')
            neg_ports = 1+8

        # forward & right
        elif k == ord('q'):
            cmd_api("x1x1",skipp_zeros=False)
            drwaw_keys(window, 1, 'q')
            neg_ports = 1 + 4

        else:
            count +=1 
            if neg_ports > 0 :
                count = 0
                neg_ports = 0
        
        if count > reset_threshold:
            cmd_api("0000",skipp_zeros=False)
            count = 0
            drwaw_keys(window, 0)

        drwaw_keys(window, None)
        cv2.imshow(gui_name,window)
    
    # exited, cloese all
    cv2.destroyAllWindows()


if __name__ == "__main__":
   main()