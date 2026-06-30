"""
config.py - Global constants, asset-free color palettes, and tracking variables.
"""
import math

WIDTH, HEIGHT = 1024, 700
FPS = 60
GROUND_Y = -250.0
TOTAL_DUR = 90.0

# Color Palette Definitions
C_SKIN = (0.76, 0.52, 0.30)
C_SKIN_DK = (0.65, 0.42, 0.28)
C_SHIRT = (0.85, 0.82, 0.75)
C_PANTS = (0.30, 0.20, 0.12)
C_GREEN = (0.00, 0.61, 0.23)
C_YELLOW = (0.99, 0.82, 0.09)
C_RED = (0.94, 0.13, 0.09)
C_GOLD = (0.83, 0.63, 0.09)
C_WOOD = (0.50, 0.30, 0.14)
C_WOOD_DK = (0.30, 0.18, 0.08)
C_BREAD = (0.87, 0.72, 0.43)
C_CLAY_BLK = (0.10, 0.06, 0.01)
C_GND_G = (0.30, 0.55, 0.18)
C_GRASS = (0.20, 0.58, 0.10)
C_SKY_T = (0.30, 0.55, 0.88)
C_SKY_B = (0.60, 0.78, 0.95)
C_WALL = (0.65, 0.52, 0.42)
C_THATCH = (0.55, 0.42, 0.25)
C_DOOR = (0.35, 0.22, 0.12)
C_WHITE = (1.0, 1.0, 1.0)
C_BLACK = (0.0, 0.0, 0.0)
C_TRUNK = (0.35, 0.20, 0.10)
C_LEAF = (0.15, 0.50, 0.10)
C_LEAF2 = (0.10, 0.42, 0.07)
C_SUN = (1.0, 0.85, 0.2)
C_SUN_GL = (1.0, 0.93, 0.55)
C_KNOB = (0.85, 0.15, 0.10)
C_HAIR = (0.10, 0.05, 0.0)
C_MOUTH = (0.50, 0.30, 0.20)
C_TENT = (0.85, 0.75, 0.60)
C_TENT_STRIPE = (0.15, 0.45, 0.15)
C_BASKET = (0.60, 0.40, 0.20)
C_GRAIN = (0.90, 0.85, 0.60)
C_ETAN_COAL = (0.15, 0.10, 0.05)
C_GIRL_DRESS = (0.95, 0.90, 0.85)
C_SMOKE_THICK = (0.65, 0.65, 0.65)
RAINBOW = [(1,.0,.0), (1,.5,.0), (1,1,.0), (.0,.8,.0), (.0,.4,1), (.3,.0,.8), (.5,.0,1)]
C_FIRE_O = (1.0, 0.4, 0.0)
C_FIRE_Y = (1.0, 0.8, 0.0)

# Layout Setup
WOMAN_BASE_X = -120.0
WOMAN_HIP_SIT = GROUND_Y + 15
WOMAN_HIP_STAND = GROUND_Y + 72
BOY_SC = 0.55
DANCER_HIP_SIT = GROUND_Y + 10
DANCER_HIP_STAND = GROUND_Y + 40
DANCER_START = WIDTH / 2 + 140
DANCER_CX = 160.0
DANCER_R = 80.0
DANCER_ANGLES_DEG = [220, 252, 284, 316, 348] 
DANCER_LINE_X = [DANCER_CX + DANCER_R * math.cos(math.radians(a)) for a in DANCER_ANGLES_DEG]

TABLE_X = -120.0
cupPositions = [TABLE_X - 52 + i*14 for i in range(8)]

NB_BASE_Y = GROUND_Y + 15
NB_COORDS = [
    (-390, NB_BASE_Y + 30),
    (-355, NB_BASE_Y + 12),
    (-315, NB_BASE_Y + 2),
    (-275, NB_BASE_Y + 8),
    (-240, NB_BASE_Y + 24)
]

# Tracked Dynamic States
# and changing values
woman_cur_x = WOMAN_BASE_X
e4_woman_y = WOMAN_HIP_SIT
rightArmAngle = -15.0
rightForeArmAngle = -10.0
leftArmAngle = 35.0
leftForeArmAngle = 18.0
headAngle = 0.0
jebenaAngle = 0.0
hasBread = False
coffeeFlow = False
holdingCup = False
servedCupsCount = 0
