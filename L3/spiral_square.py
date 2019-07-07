from turtle import *
from random import *

setup(1.0, 1.0, 0, 0)  # 画布全屏
bgcolor("black")  # 背景色
speed(0)  # 速度
hideturtle()

n = 2000
for i in range(n):
    if i%2 == 0:
        color('red')
    else:
        color('white')
    forward(i)
    right(91)
