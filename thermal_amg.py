 
import os
import math
import time
from time import sleep
import sys

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#import os
# Tell the RPi to use the TFT screen and that it's a touchscreen device
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')



pos_x = 1
pos_y = 0
#import os
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pos_x,pos_y)

 
rly_grn = 18
rly_red = 15
GPIO.setup(rly_red, GPIO.OUT)
GPIO.setup(rly_grn, GPIO.OUT) # GPIO Assign mode
GPIO.output(rly_grn, GPIO.HIGH) # out
GPIO.output(rly_red, GPIO.HIGH)

import busio
import board
 
import numpy as np
import pygame
from scipy.interpolate import griddata

from colour import Color
 
import adafruit_amg88xx
 
i2c_bus = busio.I2C(board.SCL, board.SDA)
 
#low range of the sensor (this will be blue on the screen)
#MINTEMP = 26.
MINTEMP = 34.
 
#high range of the sensor (this will be red on the screen)
#MAXTEMP = 32.
#MAXTEMP = 37.
MAXTEMP = 38
 
#how many color values we can have
COLORDEPTH = 1024
 
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
 
#initialize the sensor
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)
 
# pylint: disable=invalid-slice-index
points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
# pylint: enable=invalid-slice-index
 
#sensor is an 8x8 grid so lets do a square
height = 240
#height = 300
width = 240
#width = 240
 
#the list of colors we can choose from
blue = Color("indigo")
ggreen = (0,255,0)
bblue = (0,0,128)
rred = (255,0,0)
colors = list(blue.range_to(Color("red"), COLORDEPTH))
 
#create the array of colors
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
 
displayPixelWidth = width / 30
displayPixelHeight = height / 30
 
#lcd = pygame.display.set_mode((width, height))
lcd = pygame.display.set_mode((800, 440))
#lcd = pygame.display.set_mode((800, 480))
#lcd = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
 
lcd.fill((255, 0, 0))
pygame.display.set_caption('Thermal Scanner v1.0') 
pygame.display.update()
pygame.mouse.set_visible(False)
 
lcd.fill((0, 0, 0))
pygame.display.update()
 
#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
 
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
#let the sensor initialize
time.sleep(.1)
 


font = pygame.font.Font('freesansbold.ttf', 32)


def displayTxt(sts,sts2):
#   sts  = " "

   lcd.fill((0, 0, 0))
   text2 = font.render(sts, True, ggreen, bblue)
   textRect2 = text2.get_rect()
   textRect2.center = (460, 270)
  
   text3 = font.render(sts2, True, rred, bblue)
   textRect3 = text3.get_rect()
   textRect3.center = (460, 360)

   lcd.blit(text2, textRect2)
   lcd.blit(text3, textRect3)


def cleanAndExit():
  print("Cleaning...")
  GPIO.cleanup()
  print("Bye")
  sys.exit()


def highest(a):
  max = a[0]
  for i in a:
    if i>max:
        max = i
        return float(max)
#  print max


while True:
 try: 
    #read the pixels
    pixels = []
    for row in sensor.pixels:
        pixels = pixels + row
        pr = pixels + row
        max_temp = max(["{0:.1f}".format(temp) for temp in pr])
        min_temp = min(["{0:.1f}".format(temp) for temp in pr])
#        time.sleep(1)
#        max_temp = highest(["{0:.1f}".format(temp) for temp in row])
#        print(max_temp)
        max_msg = (f"High: {max_temp} °C ")
        min_msg = (f"Low:  {min_temp} °C ")





        text = font.render(max_msg, True, ggreen, bblue)

        textRect = text.get_rect()
        textRect.center = (500, 90)
        lcd.blit(text, textRect)

        text4 = font.render(min_msg, True, ggreen, bblue)

        textRect4 = text4.get_rect()
        textRect4.center = (500, 180)
        lcd.blit(text4, textRect4)

    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
#    print (max(pixels)) 
    #perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
#    print(max(bicubic)) 
    #draw everything
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                             (displayPixelHeight * ix, displayPixelWidth * jx,
                              displayPixelHeight, displayPixelWidth))
 
    pygame.display.update()
    if(float(max_temp) > 37.5):
          #displayTxt()
          displayTxt(" ","Fever")

#          pygame.display.update()
#          sleep(2)
          GPIO.output(rly_grn, GPIO.LOW) # out
          GPIO.output(rly_red, GPIO.LOW)
#          sleep(5)
    elif(float(max_temp) < 37.5):
          displayTxt("Normal", " ")
          GPIO.output(rly_grn, GPIO.HIGH) # out
          GPIO.output(rly_red, GPIO.HIGH)

 except(KeyboardInterrupt, SystemExit):
  cleanAndExit()
