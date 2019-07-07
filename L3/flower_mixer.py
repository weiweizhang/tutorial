from turtle import *
from random import *

setup(1.0, 1.0, 0, 0)  # 画布全屏
bgcolor("black")  # 背景色
speed(0)  # 速度
hideturtle() # 隐藏小海龟

# 抬起笔，空降到某个坐标点
def jump(x, y):
    penup()
    goto(x, y)
    pendown()
    
# flower1
def draw_flw1(color_val, length, steps):
    speed(10)
    color(color_val)
    pensize(3)
    for i in range(10):
        for i in range(4):
            circle(length, steps=steps)
            right(100)

# flower2
def draw_flw2(color1, color2, length, psize):
    speed(10)
    x = xcor()
    y = ycor()
    pensize(psize)
    for i in range(10):
        seth(i*36)
        color(color1)
        forward(length)
        right(60)
        color(color2)
        forward(length/2)
        goto(x,y)
            
# flower3
def draw_flw3(color1, color2, length, psize):
    speed(10)
    x = xcor()
    y = ycor()
    pensize(psize)
    for i in range(20):
        seth(i*9)
        for j in range(2):
            color(color1)
            forward(length)
            # 三角形
            circle(10, steps=3)
            right(60)
            color(color2)
            forward(length/2)
            goto(x,y)
            right(120)
            
# flower4
def draw_flw4(color1, color2, length, psize):
    speed(0)
    x = xcor()
    y = ycor()
    pensize(psize)
    for i in range(20):
        seth(i*9)
        for j in range(2):
            color(color1)
            forward(length)
            # 三角形
            circle(10, steps=3)
            right(60)
            color(color2)
            forward(length)
            jump(x,y)
            right(120)
                      
# flower5
def draw_flw5(color1, color2, length, psize):
    speed(0)
    x = xcor()
    y = ycor()
    pensize(psize)
    for i in range(9):
        seth(i*80)
        for j in range(2):
            color(color1)
            forward(length/2)
            right(60)
            forward(3)
            begin_fill()
            color(color2)
            forward(length)
            # 圆形
            circle(5)
            goto(x,y)
            end_fill()
            right(120)

# flower6
def draw_flw6(color_val, length, psize):
    speed(5)
    color(color_val)
    pensize(psize)
    for i in range(50):
        forward(length)
        forward(-length)  # 后退
        right(123)
            
# 开始画画
jump(500,200)
draw_flw1('cyan', 50, 4)
jump(0,0)
draw_flw1('light green', 100, 6)
jump(300, 0)
draw_flw2('green','cyan', 100, 3)
jump(-300, 0)
draw_flw2('purple','violet', 100, 5)
jump(-500,200)
draw_flw1('yellow', 50, 4)
jump(-500,-200)
draw_flw1('white', 50, 3)
jump(500,-200)
draw_flw1('pink', 50, 3)
jump(0,300)
draw_flw3('red', 'yellow', 100, 1)
jump(0,-300)
draw_flw4('pink', 'blue', 100, 1)
jump(-300,300)
draw_flw5('white', 'green', 50, 3)
jump(300,300)
draw_flw5('white', 'blue', 50, 3)
jump(-300,-300)
draw_flw5('yellow', 'red', 50, 3)
jump(300,-300)
draw_flw5('red', 'orange', 50, 3)
jump(-600,0)
draw_flw6('red', 100, 1)
jump(600,0)
draw_flw6('blue violet', 100, 1)
