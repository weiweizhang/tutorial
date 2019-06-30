from turtle import *

speed(0)
shape("turtle")

bgcolor("black")
colors = ["red", "yellow", "blue", "orange", "green", "purple"]
sides = 6
for i in range(720):
    pencolor(colors[i%sides])
    pensize(i/30)
    forward(i)
    #left(60 +1)
    left(55)
