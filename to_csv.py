#!/bin/python3

from datetime import datetime, timedelta
import sys
import csv
import re

# format
# 0          1              2       3         4   5        6           7  8
# 2024-06-14 13:40:42.19455 (+0200) +0.068823 +/- 0.000370 10.42.0.183 s3 no-leap

if len(sys.argv) != 4:
	print('usage: ./to_csv.py device_name input_file output_file')
	exit(1)
# csv:
# point number,    str      , str     float  float
# local timestamp, localhost, server, delta, delta_prec
fieldnames = ["timestamp", "clientname", "srvname", "delta", "delta_prec"]

with open(sys.argv[3], 'w+', newline='') as csvfile:
	csv = csv.writer(csvfile, delimiter=' ', quotechar="'",)

	csv.writerow(fieldnames)

	DEVICE = sys.argv[1]

	log_file = open(sys.argv[2], "r")

	for x in log_file:
		try:
			x = re.sub(r'\s+', ' ', x)
			tokens = x.strip().split(" ")

			if DEVICE == "DEMON":
				date, time, _, delta, _, delta_prec, srv_addr, _, _, _ = tokens
				date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
				timestamp = date.timestamp()
				hostname = "demon"
				del date, time
			elif DEVICE == "RASPI":
				offset = 60 * 60
				date, time, _, delta, _, delta_prec, srv_addr, _, _ = tokens
				date = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M:%S.%f")
				timestamp = date.timestamp() + offset
				hostname = "raspi"
				del date, time
			elif DEVICE == "LAPTOP_EDON":
				if tokens[0] == "server":
					print(tokens)
					_, ipaddr, _, _, _, delta, _, delta_prec = tokens
					delta = delta.replace(",", "")
					second_line = log_file.readline()
					if len(second_line.strip().split(" ntpdate")) != 2:
						continue
					y = second_line.strip().split(" ntpdate")
					datetime_str = y[0] + " 2024"
					timestamp = datetime.strptime(datetime_str, "%d %b %H:%M:%S %Y")
					# timestamp = datetime.strptime(y[0], "%d %b %H:%M:%S")
					srv_addr = "srv_addr"
					hostname = "edon"
					timestamp = timestamp.timestamp()
				else:
					print(tokens)
					continue
			elif DEVICE == "SAMSUNG":
				offset = 120 * 60
				print(tokens)
				if len(tokens) != 7:
					continue
				days_since_1900, seconds, elapsed, _, skew, _, _ = tokens
				reference_date = datetime(1900, 1, 1)
				timestamp = reference_date + timedelta(days=int(days_since_1900), seconds=float(seconds))
				timestamp = timestamp.timestamp() + offset
				hostname = "samsung"
				srv_addr = "greater-demon"
				delta = "{0:.6f}".format((float(skew) / 1000000))
				delta_prec = "{0:.6f}".format(float(elapsed) / 1000000)
			csv.writerow((timestamp, hostname, srv_addr, delta, delta_prec))
		except EOFError:
			break
		# except ValueError:
		#    print(tokens)
