from turtle import *
from random import *

setup(1.0, 1.0, 0, 0)  # 画布全屏
bgcolor("black")  # 背景色
speed(0)  # 速度
hideturtle() # 隐藏小海龟

# 画n个花
n = 60
for i in range(n):
    # 移动到随机一个坐标
    penup()
    goto(randint(-600, 600), randint(-400, 400))
    pendown()

    # 设置随机的颜色
    r   = randint( 0,  30) / 100.0
    g = randint( 0,  30) / 100.0
    b  = randint(50, 100) / 100.0
    pencolor((r, g, b))

    # 设置随机半径和画笔粗度
    radius = randint(10, 40)
    pensize(randint(1, 5))

    # 画一个花
    for i in range(6):
        circle(radius)
        left(60)
