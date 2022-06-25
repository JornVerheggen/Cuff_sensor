import vpython as vp
import numpy as np
import time
import sys

class Viz:
    def __init__(self):
        self.scene = vp.canvas(background=vp.vec(0.7,0.7,0.7))

        xaxis = vp.box(pos=vp.vector(.015, 0, 0), length=.03,
                    height=.001, width=0.001, color=vp.color.red)
        yaxis = vp.box(pos=vp.vector(0, .015, 0), length=.001,
                    height=.03, width=0.001, color=vp.color.green)
        zaxis = vp.box(pos=vp.vector(0, 0, .015), length=.001,
                    height=.001, width=.03, color=vp.color.blue)

        innerRing = vp.ring(
            pos=vp.vector(0, 0, 0),
            axis=vp.vector(0, 0, 1),
            radius=0.064, thickness=0.008
        )

        outerRing = vp.ring(
            pos=vp.vector(0, 0, 0),
            axis=vp.vector(0, 0, 1),
            radius=0.096, thickness=0.008
        )

        sens1 = vp.box(
            pos=vp.vector(-0.074, 0, 0),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(1, 0, 0),
            color=vp.color.yellow)

        sens2 = vp.box(
            pos=vp.vector(0.037, 0.064, 0),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(0.005, 0.00866, 0),
            color=vp.color.cyan)

        sens3 = vp.box(
            pos=vp.vector(.037, -.064, 0),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(0.005, -0.00866, 0),
            color=vp.color.magenta)

        mag1 = vp.cylinder(
            pos=vp.vector(-0.088, 0, 0),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0.01, 0, 0),
            color=vp.color.yellow)

        mag2 = vp.cylinder(
            pos=vp.vector(0.044, .0762, 0),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0.5, 0.866, 0),
            color=vp.color.cyan)

        mag3 = vp.cylinder(
            pos=vp.vector(0.044, -0.0762, 0),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0.5, -0.866, 0),
            color=vp.color.magenta)

        inner = vp.compound([innerRing, sens1, sens2, sens3])
        self.outer = vp.compound([outerRing, mag1, mag2, mag3])

        self.pointer1 = vp.arrow(pos=vp.vector(-.0342, 0, .0),      axis=vp.vector(-0.047, 0, .0), shaftwidth=0.001)
        self.pointer2 = vp.arrow(pos=vp.vector(0.0171, -0.0296180688, .0),      axis=vp.vector(0.0235, -0.0407031939, .0), shaftwidth=0.001)
        self.pointer3 = vp.arrow(pos=vp.vector(0.0171, 0.0296180688, .0),      axis=vp.vector(0.0235, 0.0407031939, .0), shaftwidth=0.001)

        self.oldRotationx = 0
        self.oldRotationy = 0
        self.oldRotationz = 0

    def setPosition(self,xyz):
        self.outer.pos = vp.vector(xyz[0], xyz[1], xyz[2])

    def setRotation(self,xyz):

        self.outer.axis = vp.vec(xyz[0],xyz[1],xyz[2])
        # rotx = xyz[0]
        # roty = xyz[1]
        # rotz = xyz[2]

        # print(rotx)

        # self.outer.rotate(angle=rotx,axis=vp.vec(1.,0.,0.))
        # self.outer.rotate(angle=roty,axis=vp.vec(0.,1.,0.))
        # self.outer.rotate(angle=rotz,axis=vp.vec(0.,0.,1.))

        # self.oldRotationx = xyz[0]
        # self.oldRotationy = xyz[1]
        # self.oldRotationz = xyz[2]


    def setMagPositions(self,positions):
        self.pointer1.axis = vp.vector(positions[0][0],positions[0][1],positions[0][2])
        self.pointer2.axis = vp.vector(positions[1][0],positions[1][1],positions[1][2])
        self.pointer3.axis = vp.vector(positions[2][0],positions[2][1],positions[2][2])