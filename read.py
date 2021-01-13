'''
Serial monitor

Author: Spandan Anupam
Date: 29 Jan 2021
'''

import serial
import time
import csv

# Change according to needs
ser = serial.Serial("/dev/cu.usbmodem14101")
ser.flushInput()
R = 'num_highn_10'
start_time = time.time()
while True:
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0: len(ser_bytes) - 2].decode("utf-8"))
    print(decoded_bytes)
    with open(f"data/data_{R}.csv", "a") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow([decoded_bytes])
