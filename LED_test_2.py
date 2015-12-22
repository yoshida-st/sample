import RPi.GPIO as GPIO

import Tkinter

GPIO.setmode(GPIO.BOARD)

LED = 40

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

p = GPIO.PWM(LED,100)

root = Tkinter.Tk()

led_val = Tkinter.DoubleVar()

led_val.set(0)

p.start(0)

def change_duty(dc):

	p.ChangeDutyCycle(led_val.get())
	
s = Tkinter.Scale(root,label = 'LED',orient = 'h',\
                  from_ =0,to = 100,variable = led_val,command = change_duty)

s.pack()

root.mainloop()

p.stop()

GPIO.cleanup()
