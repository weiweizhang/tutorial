from turtle import *
from random import *
import time

time.sleep(2)
setup(1.0, 1.0, 0, 0)  # 画布全屏
bgcolor("black")  # 背景色
speed(0)  # 速度


rotate=int(180)

def draw_circles(radius, num):
    for i in range(num):
        circle(radius)
        radius = radius - 4

def draw_flower(radius, num):
  for i in range (num):
    draw_circles(radius, 10)
    right(360/num)
    
color('#FDFEFE')
draw_flower(200, 10)

color('#FAD7A0')
draw_flower(160, 10)

color('#85C1E9')
draw_flower(120, 10)

color('#F1948A')
draw_flower(80, 10)

color('#F7DC6F')
draw_flower(40, 10)

