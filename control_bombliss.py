#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import socket
import threading


RIGHT = 22
LEFT = 4
DOWN = 17
UP = 18
A = 27
B = 15
R = 23
SEL = 14

PINS = [RIGHT, LEFT, DOWN, A, B, UP, R, SEL]
PINS_STR = ["R", "L", "D", "A", "B", "UP", "R", "S"]

#wait = 0.02
wait = 0.02
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
       	time.sleep(wait)
        GPIO.output(PINS[sel], False)
	time.sleep(wait)
	#print "Press: " + PINS_STR[sel] 
	#print PINS_STR[sel]

def move(xpos, ypos, sel):
	for i in xrange(sel):
		press(3)
	time.sleep(0.05)
	
	if xpos < 0 :
		for i in xrange(abs(xpos)):
			press(1)
			time.sleep(0.02)
	else :
		for i in xrange(xpos):
			press(0)
			time.sleep(0.02)

	time.sleep(0.05)
	down(ypos)

def down(d):
	print "down..."
	GPIO.output(PINS[2], True)
	time.sleep(0.016*d)
	GPIO.output(PINS[2], False)
	print "stop."
	#for i in xrange(d):
	#	press(2)
	#	time.sleep(0.02)

	
def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	sock.bind((host, port))
    	sock.listen(1)
	print "Waiting for connection..."
	conn, address = sock.accept()
	print "Connected by "+ str(address)
	time.sleep(0.5)
	press(3)
	#time.sleep(0.05)
	#down(10)
	while 1:
		msg = conn.recv(30)
		print "recv.", msg
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
	while 1:
		comm = raw_input("0:right, 1:left, 2:down, 3:A, 4:B, 5:UP, 6:R, 7:SELECT, g:start -> ")
        	if comm == "g":
                	main()
                	break
        	else:
              		press(int(comm))
