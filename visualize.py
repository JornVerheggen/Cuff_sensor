import vpython as vp

import numpy as np
import time

def init():
    xaxis = vp.box(pos=vp.vector(15,0,0),length=30, height=1, width=1,color=vp.color.red)
    yaxis = vp.box(pos=vp.vector(0,15,0),length=1, height=30, width=1,color=vp.color.green)
    zaxis = vp.box(pos=vp.vector(0,0,15),length=1, height=1, width=30,color=vp.color.blue)

    innerRing = vp.ring(
            pos=vp.vector(0,0,0),
            axis=vp.vector(0,0,1),
            radius=64, thickness=10
            )

    outerRing = vp.ring(
            pos=vp.vector(0,0,0),
            axis=vp.vector(0,0,1),
            radius=96, thickness=8
            )

    sens1 = vp.box(
            pos=vp.vector(74,0,0),
            length=3,
            height=8,
            width=8,
            axis=vp.vector(1,0,0),
            color=vp.color.yellow)

    sens2 = vp.box(
            pos=vp.vector(-37,64,0),
            length=3,
            height=8,
            width=8,
            axis=vp.vector(-0.5,0.866,0),
            color=vp.color.cyan)

    sens3 = vp.box(
            pos=vp.vector(-37,-64,0),
            length=3,
            height=8,
            width=8,
            axis=vp.vector(-0.5,-0.866,0),
            color=vp.color.magenta)

    mag1 = vp.cylinder(
            pos=vp.vector(88,0,0),
            length=4,
            height=8,
            width=8,
            axis=vp.vector(1,0,0),
            color=vp.color.yellow)

    mag2 = vp.cylinder(
            pos=vp.vector(-44,76.2,0),
            length=4,
            height=8,
            width=8,
            axis=vp.vector(-0.5,0.866,0),
            color=vp.color.cyan)

    mag3 = vp.cylinder(
            pos=vp.vector(-44,-76.2,0),
            length=4,
            height=8,
            width=8,
            axis=vp.vector(-0.5,-0.866,0),
            color=vp.color.magenta)

    inner = vp.compound([innerRing,sens1,sens2,sens3])
    global outer
    outer = vp.compound([outerRing,mag1,mag2,mag3])

def setOuterAxis(x,y,z):
    
    outer.axis = vp.vector(x,y,z)