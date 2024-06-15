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
DEVICE = sys.argv[1]
while True:
    try:
        x=input()
        tokens = x.strip().split(" ")
        
        if DEVICE == "DEMON":
            date,time,_,delta,_,delta_prec,srv_addr,_,_,_=tokens
            date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
            timestamp = date.timestamp()
            del date,time
        elif DEVICE == "RASPI":
            date,time,_,delta,_,delta_prec,srv_addr,_,_=tokens
            date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
            timestamp = date.timestamp()
            del date,time
        elif DEVICE == "LAPTOP_EDON":
            if tokens[0] == "server":
                _,ipaddr,_,_,_,delta,_,delta_prec = tokens
                y = input().strip().split(" ntpdate")
                datetime_str = y[0] + " 2024"
                timestamp = datetime.strptime(datetime_str, "%d %b %H:%M:%S %Y")
                #timestamp = datetime.strptime(y[0], "%d %b %H:%M:%S")
                srv_addr="srv_addr"
                hostname="edon"
                timestamp = timestamp.timestamp()
        elif DEVICE == "SAMSUNG":
            pass
    
        csv.writerow((timestamp, hostname, srv_addr, delta,delta_prec))
    except EOFError: break
    #except ValueError:
    #    print(tokens)

