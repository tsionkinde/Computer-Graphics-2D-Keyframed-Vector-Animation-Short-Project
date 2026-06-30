"""
main.py - Primary Engine Entrypoint. Runs rendering loops and system state polling.
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

import config
from utils import (drawCircle, drawEllipse, drawRectangle, drawCustomLimb, 
                   gl_line, gl_arc, gl_tri)
from animations import get_dancers, get_neighbors, update_woman

def draw_sun(x, y, t):
    glColor3fv(config.C_SUN)
    glPushMatrix(); glTranslatef(x, y, 0); drawCircle(35); glPopMatrix()
    glColor4f(config.C_SUN_GL[0], config.C_SUN_GL[1], config.C_SUN_GL[2], 0.4)
    for i in range(12):
        a = t * 0.15 + i * math.pi / 6
        glPushMatrix(); glTranslatef(x, y, 0); glRotatef(math.degrees(a), 0, 0, 1)
        gl_tri(0, 35, -7, 55, 7, 55); glPopMatrix()
      # creating loops 

def draw_rainbow(cx, cy):
    for i, c in enumerate(config.RAINBOW):
        r = 220 + i * 8
        glColor4f(c[0], c[1], c[2], 0.30)
        glLineWidth(7)
        glPushMatrix(); glTranslatef(cx, cy, 0)
        gl_arc(r, 0.05, math.pi - 0.05, 64)
        glPopMatrix()
    glLineWidth(1)

def draw_gojo(x, y, w, h):
    glColor3fv(config.C_WALL)
    glPushMatrix(); glTranslatef(x, y + h * 0.275, 0); drawRectangle(w, h * 0.55); glPopMatrix()
    glColor3fv(config.C_THATCH)
    glBegin(GL_TRIANGLES)
    glVertex2f(x-w/2-12, y+h*0.55); glVertex2f(x+w/2+12, y+h*0.55); glVertex2f(x, y+h); glEnd()
    glColor3fv(config.C_WALL)
    for i in range(4):
        ly = y + h * 0.55 + (h * 0.45) * (i + 1) / 5
        lw = (w + 24) * (1 - (i + 1) / 5) / 2
        gl_line(x - lw, ly, x + lw, ly)
    glColor3fv(config.C_DOOR)
    glPushMatrix(); glTranslatef(x, y + h * 0.12, 0); drawRectangle(w * 0.15, h * 0.24); glPopMatrix()

def draw_tree(tx, ty, scale=1.0):
    glPushMatrix()
    glTranslatef(tx, ty, 0)
    glScalef(scale, scale, 1)
    glColor3fv(config.C_TRUNK)
    drawRectangle(10, 70)
    for dx, dy, r, c in [(0,85,34,config.C_LEAF),(-20,70,26,config.C_LEAF2),(20,74,24,config.C_LEAF),(0,60,22,config.C_LEAF2)]:
        glColor3fv(c)
        glPushMatrix(); glTranslatef(dx, dy, 0); drawCircle(r); glPopMatrix()
    glPopMatrix()

def draw_bg(t):
    glBegin(GL_QUADS)
    glColor3fv(config.C_SKY_T); glVertex2f(-config.WIDTH/2, config.HEIGHT/2); glVertex2f(config.WIDTH/2, config.HEIGHT/2)
    glColor3fv(config.C_SKY_B); glVertex2f(config.WIDTH/2, config.GROUND_Y + 50); glVertex2f(-config.WIDTH/2, config.GROUND_Y + 50); glEnd()
    draw_sun(380, 270, t)
    if 4 < t < 30: draw_rainbow(0, config.GROUND_Y + 50)
    glColor3f(0.25, 0.48, 0.15)
    glBegin(GL_POLYGON); glVertex2f(-config.WIDTH/2, config.GROUND_Y + 50)
    for xp in range(int(-config.WIDTH / 2), int(config.WIDTH / 2), 5):
        yp = config.GROUND_Y + 50 + 55 + math.sin(xp * 0.005) * 35 + math.sin(xp * 0.013) * 20
        glVertex2f(xp, yp)
    glVertex2f(config.WIDTH / 2, config.GROUND_Y + 50); glEnd()

    draw_gojo(-420, config.GROUND_Y + 60, 40, 45)
    draw_gojo(-280, config.GROUND_Y + 80, 32, 38)
    draw_gojo(-80, config.GROUND_Y + 105, 35, 40)
    draw_gojo(50, config.GROUND_Y + 115, 30, 35)
    draw_gojo(200, config.GROUND_Y + 100, 28, 38)
    draw_gojo(350, config.GROUND_Y, 80, 90)

    draw_tree(-360, config.GROUND_Y + 80, 0.8)
    draw_tree(-200, config.GROUND_Y + 90, 0.9)
    draw_tree(160, config.GROUND_Y + 90, 1.0)
    draw_tree(280, config.GROUND_Y + 75, 0.85)

    glColor3fv(config.C_GND_G)
    glBegin(GL_QUADS)
    glVertex2f(-config.WIDTH / 2, config.GROUND_Y); glVertex2f(config.WIDTH / 2, config.GROUND_Y)
    glVertex2f(config.WIDTH / 2, -config.HEIGHT / 2); glVertex2f(-config.WIDTH / 2, -config.HEIGHT / 2); glEnd()

    glColor3fv(config.C_GRASS)
    for i in range(120):
        gx = (i * 47.3) % config.WIDTH - config.WIDTH / 2; gh = 4 + math.sin(i * 2.7) * 3
        gl_line(gx, config.GROUND_Y, gx + math.sin(t + i) * 2, config.GROUND_Y + gh)

def draw_ceremony_env(t):
    cx, cy = config.WOMAN_BASE_X, config.GROUND_Y
    glColor3fv(config.C_TENT)
    glBegin(GL_POLYGON)
    glVertex2f(cx - 180, cy + 140); glVertex2f(cx + 180, cy + 140)
    glVertex2f(cx + 200, cy + 110); glVertex2f(cx - 200, cy + 110)
    glEnd()
    for i in range(9):
        x_off = -160 + i * 40
        glColor3fv(config.C_TENT_STRIPE)
        glBegin(GL_POLYGON)
        glVertex2f(cx + x_off, cy + 139); glVertex2f(cx + x_off + 15, cy + 139)
        glVertex2f(cx + x_off + 18, cy + 111); glVertex2f(cx + x_off - 3, cy + 111)
        glEnd()
    glColor3fv(config.C_WOOD_DK)
    glPushMatrix(); glTranslatef(cx - 180, cy + 75, 0); drawRectangle(5, 140); glPopMatrix()
    glPushMatrix(); glTranslatef(cx + 180, cy + 75, 0); drawRectangle(5, 140); glPopMatrix()

    glColor3f(0.72, 0.53, 0.11)
    glBegin(GL_POLYGON)
    glVertex2f(cx - 190, cy + 5); glVertex2f(cx + 190, cy + 5)
    glVertex2f(cx + 190, cy - 8); glVertex2f(cx - 190, cy - 8); glEnd()
    glColor3f(0.65, 0.45, 0.08)
    for i in range(19): lx = cx - 180 + i * 20; gl_line(lx, cy - 8, lx, cy + 5)

    def draw_basket(bx, by, sc):
        glColor3fv(config.C_BASKET)
        glPushMatrix(); glTranslatef(bx, by, 0); glScalef(sc, sc, 1)
        glBegin(GL_POLYGON); glVertex2f(-15, 0); glVertex2f(15, 0); glVertex2f(12, 18); glVertex2f(-12, 18); glEnd()
        glColor3fv(config.C_GRAIN)
        glPushMatrix(); glTranslatef(0, 16, 0); drawEllipse(12, 4); glPopMatrix()
        glPopMatrix()

    draw_basket(cx - 150, cy + 5, 1.2); draw_basket(cx - 120, cy + 5, 1.0)
    draw_basket(cx + 130, cy + 5, 1.0); draw_basket(cx + 155, cy + 5, 0.8)

    def draw_bread_stack(bx, by, count):
        for i in range(count):
            glColor3f(0.88 - i * 0.05, 0.72 - i * 0.05, 0.43 - i * 0.05)
            glPushMatrix(); glTranslatef(bx, by + i * 4, 0); drawEllipse(18, 3); glPopMatrix()

    draw_bread_stack(cx + 80, cy + 5, 5); draw_bread_stack(cx + 115, cy + 5, 4)

def draw_fire_and_smoke(t):
    fx, fy = config.TABLE_X + 22, config.GROUND_Y - 24
    glColor3fv(config.C_CLAY_BLK)
    glPushMatrix(); glTranslatef(fx, fy, 0); drawRectangle(20, 10); glPopMatrix()
    for i in range(5):
        fl_h = 10 + math.sin(t * 15 + i) * 6
        fl_w = 4 + math.cos(t * 8 + i) * 2
        off_x = fx - 8 + i * 4
        glColor3fv(config.C_FIRE_O if i % 2 == 0 else config.C_FIRE_Y)
        gl_tri(off_x - fl_w, fy + 5, off_x + fl_w, fy + 5, off_x, fy + 5 + fl_h)

    smoke_x = fx
    for i in range(12):
        ph = (t * 0.35 + i * 0.5) % 3.0
        sx = smoke_x + math.sin(ph * 2.5) * 12
        sy = fy + 8 + ph * 35
        r = 5 + ph * 6
        a = max(0, 0.5 * (1.0 - ph / 3.0))
        glColor4f(config.C_SMOKE_THICK[0], config.C_SMOKE_THICK[1], config.C_SMOKE_THICK[2], a)
        glPushMatrix(); glTranslatef(sx, sy, 0); drawCircle(r); glPopMatrix()

def drawTableAndCups():
    glColor3f(0.42, 0.22, 0.05)
    glPushMatrix(); glTranslatef(config.TABLE_X, config.GROUND_Y - 15, 0); drawRectangle(190, 14); glPopMatrix()
    
    for idx, cpx in enumerate(config.cupPositions):
        if idx < config.servedCupsCount:
            continue
        glPushMatrix(); glTranslatef(cpx, config.GROUND_Y - 4, 0)
        if idx == config.servedCupsCount and config.coffeeFlow:
            glColor3f(1.0, 1.0, 1.0); glPushMatrix(); drawEllipse(10, 3); glPopMatrix()
        glColor3f(0.95, 0.95, 0.95)
        glBegin(GL_POLYGON)
        glVertex2f(-6, 0); glVertex2f(6, 0); glVertex2f(4, -10); glVertex2f(-4, -10); glEnd()
        glColor3f(0.22, 0.08, 0.0)
        glPushMatrix(); glTranslatef(0, -1, 0); drawEllipse(4.5, 1.5); glPopMatrix()
        glPopMatrix()

def drawJebena(t):
    if t < 37: return
    if t < 43 or t >= 51:
        jx, jy = config.TABLE_X + 22, config.GROUND_Y + 12
        j_rot = 0.0
    else:
        shoulder_x = config.woman_cur_x + 22
        shoulder_y = config.e4_woman_y + 35
        a1 = math.radians(config.rightArmAngle)
        ex = shoulder_x + math.sin(a1) * 28
        ey = shoulder_y - math.cos(a1) * 28
        a2 = math.radians(config.rightArmAngle + config.rightForeArmAngle)
        jx = ex + math.sin(a2) * 24
        jy = ey - math.cos(a2) * 24
        j_rot = config.jebenaAngle

    glPushMatrix()
    glTranslatef(jx, jy, 0); glRotatef(j_rot, 0, 0, 1)
    glScalef(-1, 1, 1); glTranslatef(2, 4, 0)
    glColor3fv(config.C_CLAY_BLK); drawEllipse(12, 16)
    glBegin(GL_POLYGON); glVertex2f(-3, 16); glVertex2f(3, 16); glVertex2f(3, 30); glVertex2f(-3, 30); glEnd()
    glPushMatrix(); glTranslatef(0, 30, 0); drawCircle(4); glPopMatrix()
    glBegin(GL_POLYGON); glVertex2f(10, -2); glVertex2f(24, 2); glVertex2f(24, 6); glVertex2f(10, 4); glEnd()
    
    if config.coffeeFlow and 43 <= t < 51:
        glColor3f(0.24, 0.10, 0.0); glLineWidth(3.5)
        glBegin(GL_LINES)
        glVertex2f(21, -6)
        glVertex2f(10, -48)
        glEnd()
        glLineWidth(1)
    glPopMatrix()

def draw_boy(x, y, sc, pose, stick=False, stick_lift=0.0, bread=False):
    hr = 20 * sc; nl = 6 * sc; nw = 10 * sc; th = 45 * sc; ttw = 36 * sc; tbw = 40 * sc
    ua = 25 * sc; la = 22 * sc; ul = 32 * sc; ll = 30 * sc; lw = 10 * sc; so = 20 * sc; ho = 10 * sc
    glPushMatrix(); glTranslatef(x, y, 0)
    for side, ha, ka in [(-1, pose['lh'], pose['lk']), (1, pose['rh'], pose['rk'])]:
        glPushMatrix()
        glTranslatef(ho * side, 0, 0); glRotatef(ha, 0, 0, 1)
        glColor3fv(config.C_PANTS); drawRectangle(lw, ul); glTranslatef(0, -ul, 0); glRotatef(ka, 0, 0, 1)
        glColor3fv(config.C_PANTS); drawRectangle(lw * 0.8, ll); glTranslatef(0, -ll, 0)
        glColor3f(0.10, 0.05, 0.02); drawRectangle(12 * sc, 5 * sc)
        glPopMatrix()
    glPushMatrix(); glRotatef(pose['to'], 0, 0, 1)
    glPushMatrix(); glTranslatef(so, th - 8 * sc, 0); glRotatef(pose['rs'], 0, 0, 1)
    glColor3fv(config.C_SKIN); drawCustomLimb(lw, ua); glTranslatef(0, -ua, 0); glRotatef(pose['re'], 0, 0, 1)
    drawCustomLimb(lw * 0.8, la); glTranslatef(0, -la, 0)
    glColor3fv(config.C_SKIN); drawCircle(4 * sc)
    glPopMatrix()
    glColor3fv(config.C_SHIRT)
    glBegin(GL_QUADS)
    glVertex2f(-ttw / 2, 0); glVertex2f(ttw / 2, 0)
    glVertex2f(tbw / 2, th); glVertex2f(-ttw / 2, th); glEnd()
    glPushMatrix(); glTranslatef(-so, th - 8 * sc, 0); glRotatef(pose['ls'], 0, 0, 1)
    glColor3fv(config.C_SKIN); drawCustomLimb(lw, ua); glTranslatef(0, -ua, 0); glRotatef(pose['le'], 0, 0, 1)
    drawCustomLimb(lw * 0.8, la); glTranslatef(0, -la, 0)
    if stick:
        glPushMatrix()
        glRotatef(-pose['ls'], 0, 0, 1)
        glTranslatef(0, 15 + stick_lift, 0)
        glColor3fv(config.C_WOOD); drawRectangle(4 * sc, 75 * sc)
        glTranslatef(0, 37 * sc, 0); glColor3fv(config.C_KNOB); drawCircle(3 * sc)
        glPopMatrix()
    if bread:
        glColor3fv(config.C_BREAD); glPushMatrix(); glTranslatef(8, 12, 0); drawCircle(7 * sc); glPopMatrix()
    glColor3fv(config.C_SKIN); drawCircle(4 * sc)
    glPopMatrix()
    glColor3fv(config.C_SKIN); drawRectangle(nw, nl)
    glPushMatrix(); glTranslatef(0, th + nl, 0); glRotatef(pose['hd'], 0, 0, 1)
    glColor3fv(config.C_HAIR); drawCircle(hr + 4 * sc)
    glColor3fv(config.C_SKIN); drawCircle(hr)
    glColor3f(0.1, 0.0, 0.0)
    glPushMatrix(); glTranslatef(-5 * sc, 3 * sc, 0); drawCircle(2 * sc); glPopMatrix()
    glPushMatrix(); glTranslatef(5 * sc, 3 * sc, 0); drawCircle(2 * sc); glPopMatrix()
    glColor3fv(config.C_HAIR)
    glPushMatrix(); glTranslatef(0, hr * 0.35, 0); drawCircle(hr * 0.85); glPopMatrix()
    glPopMatrix(); glPopMatrix(); glPopMatrix()

def draw_girl(x, y, sc, pose, bread=False, cup=False):
    hr = 18 * sc; nl = 5 * sc; nw = 8 * sc; th = 35 * sc
    ua = 20 * sc; la = 18 * sc; ul = 28 * sc; ll = 26 * sc; lw = 8 * sc; so = 16 * sc
    dress_bottom = config.GROUND_Y - y
    glPushMatrix(); glTranslatef(x, y, 0)
    glColor3fv(config.C_GIRL_DRESS)
    glBegin(GL_POLYGON)
    glVertex2f(-18, 0); glVertex2f(18, 0); glVertex2f(20, dress_bottom); glVertex2f(-20, dress_bottom)
    glEnd()
    glPushMatrix(); glRotatef(pose['to'], 0, 0, 1)
    for side, ra, ea in [(-1, pose['ls'], pose['le']), (1, pose['rs'], pose['re'])]:
        glPushMatrix()
        glTranslatef(side * so, th - 6 * sc, 0); glRotatef(ra, 0, 0, 1)
        glColor3fv(config.C_SKIN); drawCustomLimb(lw, ua); glTranslatef(0, -ua, 0)
        glRotatef(ea, 0, 0, 1)
        drawCustomLimb(lw * 0.8, la); glTranslatef(0, -la, 0)
        if bread: glColor3fv(config.C_BREAD); drawCircle(5 * sc)
        if cup:
            glColor3fv(config.C_WHITE)
            glPushMatrix(); glTranslatef(0, 2, 0); drawCircle(5 * sc); glPopMatrix()
        glColor3fv(config.C_SKIN); drawCircle(3 * sc)
        glPopMatrix()
    glColor3fv(config.C_GIRL_DRESS)
    glBegin(GL_POLYGON)
    glVertex2f(-14, 0); glVertex2f(14, 0); glVertex2f(18, th); glVertex2f(-18, th); glEnd()
    glColor3fv(config.C_SKIN); drawRectangle(nw, nl)
    glPushMatrix(); glTranslatef(0, th + nl, 0); glRotatef(pose['hd'], 0, 0, 1)
    glColor3fv(config.C_HAIR); drawCircle(hr + 3 * sc)
    glColor3fv(config.C_SKIN); drawCircle(hr)
    glColor3f(0.1, 0.0, 0.0)
    glPushMatrix(); glTranslatef(-4 * sc, 3 * sc, 0); drawCircle(1.5 * sc); glPopMatrix()
    glPushMatrix(); glTranslatef(4 * sc, 3 * sc, 0); drawCircle(1.5 * sc); glPopMatrix()
    glColor3fv(config.C_HAIR); glPushMatrix(); glTranslatef(0, hr * 0.4, 0); drawCircle(hr * 0.8); glPopMatrix()
    glPopMatrix(); glPopMatrix(); glPopMatrix()

def draw_woman():
    glPushMatrix()
    glTranslatef(config.woman_cur_x, config.e4_woman_y, 0)
    dress_bottom = config.GROUND_Y - config.e4_woman_y
    glColor3f(0.0, 0.60, 0.27)
    glBegin(GL_POLYGON); glVertex2f(-20, 40); glVertex2f(20, 40); glVertex2f(24, 10); glVertex2f(-24, 10); glEnd()
    glColor3f(0.99, 0.82, 0.09)
    glBegin(GL_POLYGON); glVertex2f(-24, 10); glVertex2f(24, 10); glVertex2f(28, -20); glVertex2f(-28, -20); glEnd()
    glColor3f(0.94, 0.13, 0.09)
    glBegin(GL_POLYGON)
    glVertex2f(-28, -20); glVertex2f(28, -20); glVertex2f(32, dress_bottom); glVertex2f(-32, dress_bottom); glEnd()

    glPushMatrix(); glTranslatef(0, 58, 0); glRotatef(config.headAngle, 0, 0, 1)
    glColor3fv(config.C_HAIR); drawCircle(18)
    glPushMatrix(); glTranslatef(0, 12, 0); drawCircle(11); glPopMatrix()
    glColor3fv(config.C_SKIN); drawCircle(16)
    glColor3f(0.1, 0.05, 0.0)
    glPushMatrix(); glTranslatef(-5, 3, 0); drawCircle(2.5); glPopMatrix()
    glPushMatrix(); glTranslatef(5, 3, 0); drawCircle(2.5); glPopMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix(); glTranslatef(-4.2, 4, 0); drawCircle(1.0); glPopMatrix()
    glPushMatrix(); glTranslatef(5.8, 4, 0); drawCircle(1.0); glPopMatrix()
    glColor3fv(config.C_HAIR); glLineWidth(2.0)
    gl_line(-8, 7, -2, 8); gl_line(2, 8, 8, 7); glLineWidth(1.0)
    glColor3fv(config.C_SKIN_DK); gl_line(0, 2, 2, -3)
    glColor3fv(config.C_MOUTH)
    glPushMatrix(); glTranslatef(0, -6, 0); drawEllipse(4, 1.5); glPopMatrix()
    glColor3fv(config.C_SKIN)
    glPushMatrix(); glTranslatef(-16, 0, 0); drawCircle(3); glPopMatrix()
    glColor3fv(config.C_GOLD)
    glPushMatrix(); glTranslatef(-16, -4, 0); drawCircle(2); glPopMatrix()
    glPushMatrix(); glTranslatef(16, -4, 0); drawCircle(2); glPopMatrix()
    glPopMatrix()

    glPushMatrix(); glTranslatef(-22, 35, 0); glRotatef(config.leftArmAngle, 0, 0, 1)
    glColor3fv(config.C_SKIN); drawCustomLimb(9, 26); glPopMatrix()

    glPushMatrix(); glTranslatef(22, 35, 0); glRotatef(config.rightArmAngle, 0, 0, 1)
    glColor3fv(config.C_SKIN); drawCustomLimb(10, 28)
    glTranslatef(0, -28, 0); glRotatef(config.rightForeArmAngle, 0, 0, 1)
    drawCustomLimb(9, 24)

    if config.hasBread:
        glColor3fv(config.C_BREAD); glPushMatrix(); glTranslatef(0, -24, 0); drawCircle(11); glPopMatrix()
    if config.holdingCup:
        glColor3fv(config.C_WHITE); glPushMatrix(); glTranslatef(0, -24, 0); drawCircle(5); glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def draw_vignette():
    for i in range(4):
        r = 350 - i * 50; a = 0.07 * (i + 1)
        glColor4f(0, 0, 0, a)
        glBegin(GL_QUADS); glVertex2f(-config.WIDTH / 2, config.HEIGHT / 2); glVertex2f(config.WIDTH / 2, config.HEIGHT / 2)
        glColor4f(0, 0, 0, 0); glVertex2f(config.WIDTH / 2, config.HEIGHT / 2 - r); glVertex2f(-config.WIDTH / 2, config.HEIGHT / 2 - r); glEnd()
        glColor4f(0, 0, 0, a)
        glBegin(GL_QUADS); glVertex2f(-config.WIDTH / 2, -config.HEIGHT / 2); glVertex2f(config.WIDTH / 2, -config.HEIGHT / 2)
        glColor4f(0, 0, 0, 0); glVertex2f(config.WIDTH / 2, -config.HEIGHT / 2 + r); glVertex2f(-config.WIDTH / 2, -config.HEIGHT / 2 + r); glEnd()

def draw_text(x, y, text, font, color=(255, 230, 200)):
    ts = font.render(text, True, color).convert_alpha()
    td = pygame.image.tostring(ts, "RGBA", True)
    w, h = ts.get_size()
    glWindowPos2f(x, y)
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, td)

def main():
    pygame.init()
    pygame.display.set_mode((config.WIDTH, config.HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Buhe Holiday - Dancers & Neighbors Coffee Ceremony")
    glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.30, 0.55, 0.88, 1.0); glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    glOrtho(-config.WIDTH / 2, config.WIDTH / 2, -config.HEIGHT / 2, config.HEIGHT / 2, -1, 1); glMatrixMode(GL_MODELVIEW)
    
    try:
        fl = pygame.font.SysFont("serif", 54, bold=True)
        fm = pygame.font.SysFont("serif", 22)
        fs = pygame.font.SysFont("sans-serif", 17)
        fu = pygame.font.SysFont("sans-serif", 19, bold=True)
    except:
        fl = pygame.font.Font(None, 54); fm = pygame.font.Font(None, 22)
        fs = pygame.font.Font(None, 17); fu = pygame.font.Font(None, 19)

    clock = pygame.time.Clock()
    playing = False
    ct = 0.0
    last_ts = None

    while True:
        dt = clock.tick(config.FPS) / 1000.0
        for ev in pygame.event.get():
            if ev.type == QUIT: pygame.quit(); sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE: pygame.quit(); sys.exit()
                if ev.key == K_SPACE:
                    playing = not playing
                    if playing and ct >= config.TOTAL_DUR: ct = 0
                if ev.key == K_RIGHT: ct = min(config.TOTAL_DUR, ct + 2)
                if ev.key == K_LEFT: ct = max(0, ct - 2)
                if ev.key == K_r: ct = 0; playing = False

        if playing:
            if last_ts is None: last_ts = pygame.time.get_ticks()
            ct += (pygame.time.get_ticks() - last_ts) / 1000.0
            if ct >= config.TOTAL_DUR:
                ct = config.TOTAL_DUR; playing = False
            last_ts = pygame.time.get_ticks()

        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        draw_bg(ct)
        sa = 0 if ct < 3 else (ct - 3 if ct < 4 else (1 if ct < 82 else (1 - (ct - 82) / 4 if ct < 86 else 0)))

        if sa > 0:
            update_woman(ct)
            dancers = get_dancers(ct)
            neighbors = get_neighbors(ct)
            draw_ceremony_env(ct)
            drawTableAndCups()
            draw_fire_and_smoke(ct)
            for nb in neighbors:
                if nb['vis']:
                    draw_girl(nb['x'], nb['y'], 0.6, nb['p'], bread=nb['brd'], cup=nb['cup'])
            draw_woman()
            for d in dancers:
                if d['vis']:
                    draw_boy(d['x'], d['y'], config.BOY_SC, d['p'], stick=True, stick_lift=d['lift'], bread=d['brd'])
            drawJebena(ct)
            
        draw_vignette()
        ta = 0 if ct < 0.5 else ((ct - 0.5) / 2.0 if ct < 2.5 else (1.0 if ct < 3.5 else (1.0 - (ct - 3.5) / 0.5 if ct < 4.0 else (0.0 if ct < 85.0 else ((ct - 85.0) / 1.5 if ct < 86.5 else 1.0)))))

        if ta > 0:
            glColor4f(0.02, 0.01, 0.005, ta * 0.5)
            glBegin(GL_QUADS)
            glVertex2f(-config.WIDTH / 2, -config.HEIGHT / 2); glVertex2f(config.WIDTH / 2, -config.HEIGHT / 2)
            glVertex2f(config.WIDTH / 2, config.HEIGHT / 2); glVertex2f(-config.WIDTH / 2, config.HEIGHT / 2)
            glEnd()
            c = int(ta * 255)
            draw_text(config.WIDTH / 2 - 200, config.HEIGHT / 2 + 50, "Buhe Holiday", fl, (c, int(c * 0.88), int(c * 0.75)))
            draw_text(config.WIDTH / 2 - 160, config.HEIGHT / 2 - 15, "In Ethiopia", fl, (c, int(c * 0.88), int(c * 0.75)))
            sub = "A Traditional Ethiopian Holiday" if ct < 4 else "Celebrating Heritage"
            draw_text(config.WIDTH / 2 - 145, config.HEIGHT / 2 - 65, sub, fm, (int(c * 0.82), int(c * 0.62), int(c * 0.09)))

        if ct > 4:
            m, s = divmod(int(ct), 60)
            draw_text(config.WIDTH / 2 - 120, config.HEIGHT / 2 - config.HEIGHT / 2 + 15, f"{m}:{s:02d} / 1:30", fu, (138, 112, 96))
            if ct < 11.5: lbl = "Boys Arrive from Right"
            elif ct < 15: lbl = "Boys Stand in Position"
            elif ct < 25: lbl = "Stick Dance"
            elif config.TOTAL_DUR > ct >= 25:
                if ct < 27: lbl = "Taking Bread"
                elif ct < 37: lbl = "Boys Leave"
                elif ct < 43: lbl = "Stove Burning & Heating"
                elif ct < 51: lbl = "Pouring Coffee into Cini"
                elif ct < 57: lbl = "Preparing Cups"
                elif ct < 85: lbl = "Serving Circular Seated Neighbors"
                else: lbl = ""
            else: lbl = ""
            draw_text(20, config.HEIGHT / 2 - config.HEIGHT / 2 + 15, f"Scene: {lbl}", fs, (184, 124, 26))

        glEnable(GL_BLEND)
        glColor4f(0.0, 0.0, 0.0, 0.75)
        glBegin(GL_QUADS)
        glVertex2f(-config.WIDTH/2, -config.HEIGHT/2); glVertex2f(-config.WIDTH/2 + 540, -config.HEIGHT/2)
        glVertex2f(-config.WIDTH/2 + 540, -config.HEIGHT/2 + 45); glVertex2f(-config.WIDTH/2, -config.HEIGHT/2 + 45)
        glEnd()
        draw_text(20, 15, "[SPACE] Play/Pause   [LEFT/RIGHT] Seek   [R] Reset   [ESC] Quit", fs, (240, 240, 245))
        pygame.display.flip()

if __name__ == "__main__":
    main()
