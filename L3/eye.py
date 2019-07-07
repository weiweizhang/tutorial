from turtle import *
from random import *

setup(1.0, 1.0, 0, 0)  # 画布全屏
bgcolor("black")  # 背景色
speed(0)  # 速度
hideturtle() # 隐藏小海龟

n = 360
for i in range(n):
    pencolor("orange")
    forward(150)
    right(50)
    pencolor("white")
    forward(120)
    left(60)
    pencolor("green")
    pensize(1.5)
    forward(150)
    right(10)

    # 回到原点
    penup()
    goto(0, 0)
    pendown()
    
    right(360*10/n + 1)
    
