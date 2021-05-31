# -*- coding: utf-8 -*-
"""
Created on Wed May 26 08:40:20 2021

@author: 오상윤
"""

from turtle import *
import sys
def draw(x,y,n,co,turn):
    shape("turtle")
    pencolor("red")
    penup()
    goto(x,y)
    pendown()
    i=0
    fillcolor(co)
    begin_fill()
    while i<n:
        if turn=='L':
            left(360/n)
        elif turn=='R':
            right(360/n)
        forward(100)
        i+=1
    end_fill()
draw(100, 100, 4, "GREEN",'R')
draw(100, 100, 3, "YELLOW",'L')
exitonclick()


