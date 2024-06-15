#!/bin/bash


SRV=192.168.0.118
OUTFILE=ntpquery.samsung.log
SLEEP_INTVL=10s

while true; do
    #sudo ntpdate -q $SRV | tee -a $OUTFILE
    adb shell /data/local/tmp/ntpclient -h $SRV -c 1 | tee -a $OUTFILE
    sleep $SLEEP_INTVL
done
