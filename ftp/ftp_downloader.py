#!/bin/python3
import argparse
import threading
import ftplib
import sys
from pwn import log

# FTP load generator: downloads the same remote file over N parallel sessions to
# produce sustained traffic through a firewall under test (traffic shaping,
# session limits, inspection throughput). Use only against lab equipment you own.
parser = argparse.ArgumentParser(description="FTP load generator: downloads one remote file over N parallel FTP sessions to generate test traffic")
parser.add_argument("-t", "--threads", type=int, dest="thread_n", help="amount of threads", required=True)
parser.add_argument("-n", "--remote_file_name", type=str, dest="remote_file_name", help="name of the remote file")
parser.add_argument("-u", "--username", type=str, dest="username", help="remote username", required=True)
parser.add_argument("-p", "--pasword", type=str, dest="password", help="remote username password", required=True)
parser.add_argument("--host", type=str, dest="host", help="remote ftp ip", required=True)

args = parser.parse_args()

def def_handler(sig, frame):
    print("\n\n[!] Saliendo..\n")
    sys.exit(1)

thread_n=int(args.thread_n) if args.thread_n != None else 0
remote_name=args.remote_file_name if args.remote_file_name != None else "padding"
host = args.host
username = args.username
password = args.password
total_size = 0

#get size 
with ftplib.FTP(host) as ftp:
    ftp.login(user=username, passwd=password)
    ftp.set_pasv(True)
    total_size = int(ftp.size(remote_name))

## initialize threads
def download_file(host, username, password, ftp_path, local_path, progress):
    
    with ftplib.FTP(host) as ftp:
        
        ftp.login(user=username, passwd=password)
        ftp.set_pasv(True)

        with open(local_path, 'wb') as local_file:
            ftp.retrbinary('RETR ' + ftp_path, local_file.write)
        
            progress.success("File downloaded")


threads = []
for n in range(thread_n):
    progress = log.progress(f"Downloading {remote_name} {n}")
    thread = threading.Thread(target=download_file, args=(host, username, password, remote_name, f"{remote_name}.{n}", progress))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All files downloaded!")
