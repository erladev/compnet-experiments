#!/bin/python3

from datetime import datetime
import socket
import sys
import csv

# format
# 0          1              2       3         4   5        6           7  8
# 2024-06-14 13:40:42.19455 (+0200) +0.068823 +/- 0.000370 10.42.0.183 s3 no-leap

# csv:
# point number,    str      , str     float  float
# local timestamp, localhost, server, delta, delta_prec
fieldnames = ("timestamp", "clientname", "srvname", "delta", "delta_prec")

hostname = socket.gethostname()
csv=csv.writer(sys.stdout, delimiter=' ', quotechar="'")

if True:
    csv.writerow(fieldnames)

while True:
    try:
        x=input()
        tokens = x.strip().split(" ")
        
        date,time,_,delta,_,delta_prec,srv_addr,_,_,_=tokens
        date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
        timestamp = date.timestamp()
        del date,time
        csv.writerow((timestamp, hostname, srv_addr, delta,delta_prec))
    except EOFError: break
    #except ValueError:
    #    print(tokens)

