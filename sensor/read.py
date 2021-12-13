import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

inputs = [7,8,10,11,12,13,15,16]

readings = [0] * len(inputs)

for i in inputs:
	
	GPIO.setup(i, GPIO.IN)
	
def read_inputs():

    for i in range(len(inputs)):
	    
	    readings[i] = 1 - GPIO.input(inputs[i])
	    
    return readings
		    

if __name__ == "__main__":

    while True:

	    for i in range(len(inputs)):
	    
		    readings[i] = GPIO.input(inputs[i])
		    
	    sleep(0.2)
	    
	    print(readings)
