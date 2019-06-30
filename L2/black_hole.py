from turtle import *

speed(0)
bgcolor("black")
color("#FF6600","#FF6600")
goto(0,-300)
begin_fill()
circle(300)
end_fill()
home()
color("black","black")

for each in range(360):
    right(1)
    circle(150)
