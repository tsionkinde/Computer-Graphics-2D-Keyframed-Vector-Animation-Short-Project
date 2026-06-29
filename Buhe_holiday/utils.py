"""
utils.py - Custom math formulas and primitive 2D vector drawing operations.
"""
import math
from OpenGL.GL import *

def lerp(a, b, t): 
    return a + (b - a) * t

def ss(t): 
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)

def cl(v, lo, hi): 
    return max(lo, min(hi, v))

def drawCircle(radius, segments=50):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        glVertex2f(radius * math.cos(a), radius * math.sin(a))
    glEnd()

def drawEllipse(rx, ry, segments=50):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)
    for i in range(segments + 1):
        a = 2 * math.pi * i / segments
        glVertex2f(rx * math.cos(a), ry * math.sin(a))
    glEnd()

def drawRectangle(width, height):
    glBegin(GL_POLYGON)
    glVertex2f(-width/2, -height/2)
    glVertex2f( width/2, -height/2)
    glVertex2f( width/2,  height/2)
    glVertex2f(-width/2, height/2)
    glEnd()

def drawCustomLimb(width, height):
    glBegin(GL_POLYGON)
    glVertex2f(-width/2, 0)
    glVertex2f(width/2, 0)
    glVertex2f(width/2, -height)
    glVertex2f(-width/2, -height)
    glEnd()

def gl_line(x1, y1, x2, y2):
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def gl_arc(r, a1, a2, s=16):
    glBegin(GL_LINE_STRIP)
    for i in range(s+1):
        a = a1 + (a2 - a1) * i / s
        glVertex2f(math.cos(a) * r, math.sin(a) * r)
    glEnd()

def gl_tri(x1, y1, x2, y2, x3, y3):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x3, y3)
    glEnd()