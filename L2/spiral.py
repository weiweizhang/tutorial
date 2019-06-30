from turtle import *

# 设置画布大小
setup(2000,1400,0,0)
bgcolor("black")
#shape("turtle")
speed(0)

hideturtle()

l = 30
for i in range(500):
    # 设置颜色
    if i % 3 == 0:
        color("red")
    elif i % 3 == 1:
        color("white")
    elif i % 3 == 2:
        color("blue")

    # 画正方形
    for each in range(4):
        forward(l)
        left(90)

    l = l+1
    left(3)
