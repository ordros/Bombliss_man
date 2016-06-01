#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import socket
import threading


RIGHT = 22
LEFT = 4
DOWN = 17
A = 27

PINS = [RIGHT, LEFT, DOWN, A]
PINS_STR = ["R", "L", "D", "A"]

wait_press = 0.02
wait_change = 0.05

host = "192.168.10.148"
port = 50000

def init():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(4, GPIO.OUT)
	for i in PINS:
		GPIO.setup(i, GPIO.OUT)

def press(sel):
    GPIO.output(PINS[sel], True)
	time.sleep(wait_press)
    GPIO.output(PINS[sel], False)
	time.sleep(wait_press)
	print "Press: " + PINS_STR[sel]

def move(xpos, ypos, sel):
	for i in xrange(sel):
		press(3)
	time.sleep(wait_change)

	if xpos < 0 :
		for i in xrange(abs(xpos)):
			press(1)
	else :
		for i in xrange(xpos):
			press(0)
	time.sleep(wait_change)
	down(ypos)

def down(d):
	for i in xrange(d):
		press(2)
		time.sleep(wait_press)


def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.bind((host, port))
    	sock.listen(1)
	print "Waiting for connection..."
	conn, address = sock.accept()
	print "Connected by "+ str(address)
	time.sleep(0.5)
	press(3)
	#time.sleep(wait_change)
	#down(10)
	while 1:
		msg = conn.recv(10)
		print "recv."
		try:
			a = msg.split("_")
			if a :
				xpos = int(a[0])
				sel = int(a[1])
				ypos = int(a[2])
				align = int(a[3])
				print xpos-align, ypos, sel
				move(xpos-align, ypos, sel)

		except Exception as e:
			print str(e)

			GPIO.cleanup()
			sock.close()
			break

		if msg == "q":
			sock.close()
			break

if __name__ == "__main__":
	init()
	main()
