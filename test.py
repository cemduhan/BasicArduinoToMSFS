import pyfirmata
import time
from SimConnect import *
import logging
from SimConnect.Enum import *
from time import sleep


def validinput(prompt):
	try:
		trt = float(prompt) * 1000
		return trt
		# there is no need to use another variable here, just return the conversion,
		# if it fail it will try again because it is inside this infinite loop
	except:
		print("Return 600")
		return 600


if __name__ == "__main__":

	print("Program Start Up")

	logging.basicConfig(level=logging.DEBUG)
	LOGGER = logging.getLogger(__name__)
	LOGGER.info("START")
	# time holder for inline commands
	ct_g = millis()

	board = pyfirmata.Arduino("COM3")
	it = pyfirmata.util.Iterator(board)
	it.start()
	# creat simconnection and pass used user classes

	print("Board Initialized")
	SpeedBluePot = board.get_pin("a:0:i")
	HeadingWhitePot = board.get_pin("a:1:i")
	AltitudeGreenPot = board.get_pin("a:2:i")
	VerticalSpeedBlackPot = board.get_pin("a:3:i")
	xAxis = board.get_pin("a:4:i")
	yAxis = board.get_pin("a:5:i")
	start = time.time()
	end = time.time()
	sw = False
	pr = True
	BL = board.get_pin('d:5:i')
	BML = board.get_pin('d:4:i')
	BMR = board.get_pin('d:3:i')
	BR = board.get_pin('d:2:i')
	time.sleep(1)
	print("Read Go")
	while True:
		if BL.read():
			if pr:
				print("Read P")
			if not sw:
				start = time.time()
			sw = True
		else:
			if pr:
				print("Read N")
			end = time.time()
			if sw:
				pr = False
				elapsed_time = time.time() - start
				print(elapsed_time)
				sw = False
	print("END")