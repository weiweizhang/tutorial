from turtle import *
from random import *

speed(0)  # 画画速度
tracer(10, 0) # 加快渲染速度
screen_width = 1920 
screen_height = 1080
setup(screen_width, screen_height, 0, 0) # 画布大小
bgpic("bg.gif") # 背景图片，注意图片文件与程序文件放在同一个目录下

def draw_snowflake(radius):
    color("white")
    pensize(radius/10)
    seth(90)
    for each in range(6):
        forward(radius)
        forward(-radius*0.4)
        left(40)
        forward(radius*0.3)
        forward(-radius*0.3)
        right(80)
        forward(radius*0.3)
        forward(-radius*0.3)
        left(40)
        forward(-radius*0.6)

        right(60)
    

# 画n个雪花
n = 30
for each in range(n):
    # 移动到 随机坐标(x,y)
    x = randint(-screen_width/2, screen_width/2)
    y = randint(-screen_height/2 + 200, screen_height/2)
    penup()
    goto(x, y)
    pendown()
    # 随机半径
    radius = randint(10, 100)
    # 画雪花
    draw_snowflake(radius)
    
