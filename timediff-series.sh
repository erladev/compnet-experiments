#!/bin/bash


SRV=ts2.univie.ac.at
OUTFILE=ntpquery.demon.log
SLEEP_INTVL=10s

while true; do
    sudo ntpdate -q $SRV | tee -a $OUTFILE
    sleep $SLEEP_INTVL
done
