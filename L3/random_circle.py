from turtle import *
from random import *
from time import *

setup(1.0, 1.0, 0, 0) # 画布大小
speed(0) # 最快速度画画
hideturtle() # 隐藏小海龟
bgcolor("black") # 画布背景
colormode(255) # 颜色模式RGB

def draw_circle():
    # 设置随机的颜色
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    color((r, g, b))
    # 随机的半径
    radius = randint(10, 100)
    # 画圆
    begin_fill()
    circle(radius) 
    end_fill()


# 画100个圆
n = 100
for i in range(n):
    # 移动到下一个位置
    penup()
    x = randint(-600, 600)
    y = randint(-400, 400)
    goto(x, y) 
    pendown()
    
    draw_circle()

# 休息1秒
sleep(1)
