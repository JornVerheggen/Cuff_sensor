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

        handCenter1 = vp.sphere(pos=vp.vector(0.05775,0,0), radius=0.003)
        handCenter2 = vp.cone(pos=vp.vector(0.05775,.0,0.01231),axis=vp.vector(0.005,0,0),radius=0.005)

        self.handPointer1 = vp.sphere(pos=vp.vector(0.05775,0,0), radius=0.003,color=vp.color.purple)
        self.handPointer2 = vp.cone(pos=vp.vector(0.05775,.0,0.01231),axis=vp.vector(0.005,0,0,),radius=0.005,color=vp.color.purple)

        innerRing = vp.ring(
            pos=vp.vector(0, 0, 0),
            axis=vp.vector(1, 0, 0),
            radius=0.064, thickness=0.008
        )

        outerRing = vp.ring(
            pos=vp.vector(0, 0, 0),
            axis=vp.vector(1, 0, 0),
            radius=0.096, thickness=0.008
        )

        sens1 = vp.box(
            pos=vp.vector(0,-0.074, 0),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(0, 1, 0),
            color=vp.color.yellow)

        sens2 = vp.box(
            pos=vp.vector(0,.037, .064),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(0,0.005, -0.00866),
            color=vp.color.magenta)

        sens3 = vp.box(
            pos=vp.vector(0,0.037, -0.064),
            length=0.003,
            height=0.008,
            width=0.008,
            axis=vp.vector(0,0.005, 0.00866),
            color=vp.color.cyan)

        mag1 = vp.cylinder(
            pos=vp.vector(0,-0.088, 0),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0, 0.001, 0),
            color=vp.color.yellow)

        mag2 = vp.cylinder(
            pos=vp.vector(0,0.044, 0.0762),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0,0.5, -0.866),
            color=vp.color.magenta)

        mag3 = vp.cylinder(
            pos=vp.vector(0,0.044, -.0762),
            length=0.004,
            height=0.008,
            width=0.008,
            axis=vp.vector(0,0.5, 0.866),
            color=vp.color.cyan)

        inner = vp.compound([innerRing, sens1, sens2, sens3])
        self.outer = vp.compound([outerRing, mag1, mag2, mag3])

        self.pointer1 = vp.arrow(pos=vp.vector(0,-.0342, 0,), axis=vp.vector(0,-0.047, 0), shaftwidth=0.001)
        self.pointer2 = vp.arrow(pos=vp.vector(0,0.0171, -0.0296180688), axis=vp.vector(0,0.0235, -0.0407031939), shaftwidth=0.001)
        self.pointer3 = vp.arrow(pos=vp.vector(0,0.0171, 0.0296180688), axis=vp.vector(0,0.0235, 0.0407031939), shaftwidth=0.001)

    def setPosition(self,xyz):
        self.outer.pos = vp.vector(xyz[0], xyz[1], xyz[2])

    def setRotation(self,xyz):
        self.outer.axis = vp.vec(xyz[0],xyz[1],xyz[2])

    def setMagPositions(self,positions):
        self.pointer1.axis = vp.vector(positions[0][0],positions[0][1],positions[0][2])
        self.pointer2.axis = vp.vector(positions[1][0],positions[1][1],positions[1][2])
        self.pointer3.axis = vp.vector(positions[2][0],positions[2][1],positions[2][2])
    
    def setHandPointer(self,homTrans):
        rot = homTrans[:3,:3]
        trans = homTrans[:3,3]

        handPos1 = np.array([0.05775,0,0])
        handPos2 = np.array([0.05775,.0,0.01231])

        newPos1 = np.matmul(handPos1,rot) + trans
        newPos2 = np.matmul(handPos2,rot) + trans
        self.handPointer1.pos = vp.vector(newPos1[0],newPos1[1],newPos1[2])
        self.handPointer2.pos = vp.vector(newPos2[0],newPos2[1],newPos2[2])