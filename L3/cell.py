from turtle import *
from random import *


setup(1.0, 1.0, 0, 0) # 画布大小
bgcolor("black")  # 背景色
speed(0) # 画画速度
hideturtle() # 隐藏小海龟
colormode(255)  # 颜色模式RGB
tracer(10, 0) # 加快渲染速度

def draw_cell():
    # 随机画笔颜色
    r = randint(0, 0)
    g = randint(10, 255)
    b = randint(10, 255)
    color((r, g, b))
        
    # 随机cell的边长
    l = randint(10, 100)
    
    # 画36个正方形，旋转叠加
    for j in range(36):
        # 画一个正方形
        for k in range(4):
            forward(l)
            left(90)
        left(10)

        
# 画n个细胞
n = 25
for i in range(n):
    # 空降到某个地点
    penup()
    goto(randint(-600, 600), randint(-400, 400))
    pendown()

    # 画细胞
    draw_cell()
    
