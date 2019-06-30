from turtle import *

shape("turtle")

length = 200
angle = 90

color("red","yellow")
begin_fill()
for each in range(4):
    forward(length)
    right(angle)
end_fill()
