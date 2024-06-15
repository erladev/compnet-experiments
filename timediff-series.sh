#!/bin/bash


SRV=10.42.0.183
OUTFILE=ntpquery.log
SLEEP_INTVL=10s

while true; do
    sudo ntpdate -q $SRV | tee -a $OUTFILE
    sleep $SLEEP_INTVL
done