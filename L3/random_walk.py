from turtle import *
from random import *

setup(1.0, 1.0, 0, 0) # 画布大小
bgcolor("black")  # 背景色
speed(0) # 画画速度
hideturtle() # 隐藏小海龟
colormode(255) # 颜色模式为RGB
pensize(2) # 画笔粗细
tracer(10, 0) # 加快渲染速度

n = 20
for i in range(n):
    # 画一个分子的运动轨迹
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    color((r,g,b))
    for j in range(2000):
        # 随机走走
        left(uniform(-90,90))
        forward(uniform(0,10))
        
    # 回到原点
    penup()
    goto(0,0)
    pendown()
