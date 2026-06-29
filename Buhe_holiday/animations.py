"""
animations.py - Core mathematical timeline logic and keyframe configurations.
"""
import math
import config
from utils import lerp, ss, cl

def def_p(): 
    return {'to':0, 'hd':0, 'ls':-5, 'le':0, 'rs':5, 're':0, 'lh':0, 'lk':0, 'rh':0, 'rk':0}

def sit_p(): 
    return {'to':0, 'hd':5, 'ls':-20, 'le':-55, 'rs':20, 're':-55, 'lh':-85, 'lk':85, 'rh':85, 'rk':-85}

def lerp_p(a, b, t):
    r = {}
    for k in a: 
        r[k] = lerp(a[k], b[k], t)
    return r

def walk_cyc(ph):
    p = def_p()
    s = math.sin(ph * 2 * math.pi)
    p['lh'] = s * 20
    p['rh'] = -s * 20
    p['lk'] = max(0, -s) * 30
    p['rk'] = max(0, s) * 30
    p['ls'] = -20 - max(0, s) * 50  
    p['rs'] = 20 + max(0, -s) * 50   
    p['le'] = -max(0, s) * 25
    p['re'] = -max(0, -s) * 25
    return p

def stick_dance(ph):
    p = def_p()
    y_off = 0.0  
    p['to'] = math.sin(ph * 4 * math.pi) * 4
    p['hd'] = -math.sin(ph * 4 * math.pi) * 3
    wave_state = 1 if (ph % 1.0) < 0.5 else -1
    p['ls'] = -80
    p['le'] = 90 * wave_state
    p['rs'] = 60 + (math.sin(ph * 2 * math.pi) * 50)
    p['re'] = -30
    return y_off, p

def get_dancers(t):
    dancers = []
    for i in range(5):
        dancers.append({
            'x': config.DANCER_LINE_X[i], 'y': config.DANCER_HIP_SIT,
            'p': sit_p(), 'vis': False, 'brd': False, 'lift': 0.0
        })
        
    if 0 <= t < 11.5:
        dur = 5.0  
        for i in range(5):
            dl = i * 1.3  
            bt = t - dl
            if bt > 0:
                dancers[i]['vis'] = True
                prog = cl(bt / dur, 0, 1)
                dancers[i]['x'] = lerp(config.DANCER_START, config.DANCER_LINE_X[i], ss(prog))
                if prog < 1.0:
                    dancers[i]['p'] = walk_cyc((bt * 1.0) % 1.0)
                    dancers[i]['y'] = config.DANCER_HIP_STAND
                else:
                    dancers[i]['x'] = config.DANCER_LINE_X[i]
                    dancers[i]['y'] = config.DANCER_HIP_STAND   
                    dancers[i]['p'] = def_p()              
            else:
                dancers[i]['vis'] = False
                
    elif 11.5 <= t < 15.0: 
        for i in range(5):
            dancers[i]['vis'] = True
            dancers[i]['x'] = config.DANCER_LINE_X[i]
            dancers[i]['y'] = config.DANCER_HIP_STAND
            dancers[i]['p'] = def_p()
            
    elif 15.0 <= t < 25:
        for i in range(5):
            dancers[i]['vis'] = True
            y_off, dancers[i]['p'] = stick_dance((t - 15.0) * 0.4)
            dancers[i]['y'] = config.DANCER_HIP_STAND + y_off
            
    elif 25 <= t < 27:
        sit_t = ss((t - 25) / 1.5)
        for i in range(5):
            dancers[i]['vis'] = True
            dancers[i]['y'] = lerp(config.DANCER_HIP_STAND, config.DANCER_HIP_SIT, sit_t)
            dancers[i]['p'] = lerp_p(def_p(), sit_p(), sit_t)

    elif 27 <= t < 37:
        bi = 2; lt = t - 27
        for i in range(5):
            if i != bi:
                dancers[i]['vis'] = True
                dancers[i]['p'] = sit_p()
                dancers[i]['y'] = config.DANCER_HIP_SIT

        meet_x = config.DANCER_CX - 20
        if lt < 2:
            stand = ss(lt / 1.5)
            dancers[bi]['y'] = lerp(config.DANCER_HIP_SIT, config.DANCER_HIP_STAND, stand)
            dancers[bi]['x'] = lerp(config.DANCER_LINE_X[bi], meet_x, stand)
            dancers[bi]['p'] = lerp_p(sit_p(), def_p(), stand)
            dancers[bi]['vis'] = True
        elif lt < 4:
            dancers[bi]['y'] = config.DANCER_HIP_STAND
            dancers[bi]['x'] = meet_x
            dancers[bi]['p'] = def_p()
            dancers[bi]['vis'] = True
        elif lt < 6:
            dancers[bi]['y'] = config.DANCER_HIP_STAND
            dancers[bi]['x'] = meet_x
            take = ss((lt - 4) / 1.0)
            dancers[bi]['p']['ls'] = lerp(-5, 65, take)
            dancers[bi]['p']['le'] = lerp(0, -35, take)
            dancers[bi]['vis'] = True
        elif lt < 7:
            dancers[bi]['brd'] = True
            dancers[bi]['y'] = config.DANCER_HIP_STAND
            dancers[bi]['x'] = meet_x
            dancers[bi]['p'] = def_p()
            dancers[bi]['vis'] = True
        elif lt < 9:
            dancers[bi]['brd'] = True
            back = ss((lt - 7) / 2.0)
            dancers[bi]['x'] = lerp(meet_x, config.DANCER_LINE_X[bi], back)
            dancers[bi]['y'] = config.DANCER_HIP_STAND
            dancers[bi]['p'] = walk_cyc((lt - 7) * 1.5 % 1.0)
            dancers[bi]['vis'] = True
        else:
            dancers[bi]['brd'] = True
            sit_t = ss((lt - 9) / 1.5)
            dancers[bi]['x'] = config.DANCER_LINE_X[bi]
            dancers[bi]['y'] = lerp(config.DANCER_HIP_STAND, config.DANCER_HIP_SIT, sit_t)
            dancers[bi]['p'] = lerp_p(def_p(), sit_p(), sit_t)
            dancers[bi]['vis'] = True
            
    elif 37 <= t < 44:
        if t < 40.0:
            for i in range(5):
                dancers[i]['vis'] = True
                dancers[i]['brd'] = (i == 2)
                dancers[i]['x'] = config.DANCER_LINE_X[i]
                y_off, dancers[i]['p'] = stick_dance((t - 34.0) * 0.4)
                dancers[i]['y'] = config.DANCER_HIP_STAND + y_off
        else:
            dur = 4.0
            walk_start_time = 40.0
            for i in range(5):
                dancers[i]['brd'] = (i == 2)
                dl = i * 0.3
                bt = t - walk_start_time - dl
                if bt > 0:
                    prog = cl(bt / dur, 0, 1)
                    if prog < 1.0:
                        dancers[i]['vis'] = True
                        dancers[i]['x'] = lerp(config.DANCER_LINE_X[i], config.DANCER_START, ss(prog))
                        dancers[i]['y'] = config.DANCER_HIP_STAND
                        dancers[i]['p'] = walk_cyc((bt * 1.8) % 1.0)
                    else:
                        dancers[i]['vis'] = False
                else:
                    dancers[i]['vis'] = True
                    dancers[i]['x'] = config.DANCER_LINE_X[i]
                    dancers[i]['y'] = config.DANCER_HIP_STAND
                    dancers[i]['p'] = def_p()
    else:
        for i in range(5): 
            dancers[i]['vis'] = False
        
    return dancers

def get_neighbors(t):
    nb = []
    for i in range(5):
        nx, ny = config.NB_COORDS[i]
        has_received = (t >= 57 + (i + 1) * 5.6)
        nb.append({
            'x': nx, 'y': ny, 'p': sit_p(),
            'vis': True, 'brd': False, 'cup': has_received
        })
    return nb

def update_woman(t):
    config.woman_cur_x = config.WOMAN_BASE_X
    config.e4_woman_y = config.WOMAN_HIP_SIT
    config.rightArmAngle = -15.0
    config.rightForeArmAngle = -10.0
    config.leftArmAngle = 35.0
    config.leftForeArmAngle = 18.0
    config.headAngle = 0.0
    config.hasBread = False
    config.coffeeFlow = False
    config.jebenaAngle = 0.0
    config.holdingCup = False
    config.servedCupsCount = 0

    if 27 <= t < 37:
        lt = t - 27; meet_x = config.DANCER_CX - 20
        if lt < 2:
            config.e4_woman_y = lerp(config.WOMAN_HIP_SIT, config.WOMAN_HIP_STAND, ss(lt / 1.5))
            config.rightArmAngle = lerp(-15, 10, ss(lt / 1.5))
            config.hasBread = True
        elif lt < 4:
            walk = ss((lt - 2) / 2.0)
            config.woman_cur_x = lerp(config.WOMAN_BASE_X, meet_x, walk)
            config.e4_woman_y = config.WOMAN_HIP_STAND
            config.rightArmAngle = math.sin(t * 0.15) * 15 - 10
        elif lt < 6:
            config.woman_cur_x = meet_x
            config.e4_woman_y = config.WOMAN_HIP_STAND
            config.rightArmAngle = lerp(10, -70, ss((lt - 4) / 1.0))
            config.rightForeArmAngle = lerp(-15, -10, ss((lt - 4) / 1.0))
            config.hasBread = True if lt < 5.4 else False
        elif lt < 9:
            back = ss((lt - 6) / 3.0)
            config.woman_cur_x = lerp(meet_x, config.WOMAN_BASE_X, back)
            config.e4_woman_y = config.WOMAN_HIP_STAND
            config.rightArmAngle = math.sin(t * 0.15) * 15 - 10
        else:
            config.woman_cur_x = config.WOMAN_BASE_X
            config.e4_woman_y = lerp(config.WOMAN_HIP_STAND, config.WOMAN_HIP_SIT, ss((lt - 9) / 1.5))
    elif 37 <= t < 43:
        ef = ss((t - 37) / 4.0)
        config.rightArmAngle = lerp(-15, -65, ef)
        config.rightForeArmAngle = lerp(-10, -35, ef)
        config.jebenaAngle = lerp(0, 10, ef)
        config.headAngle = lerp(0, -12, ef)
    elif 43 <= t < 51:
        config.rightArmAngle = -52.0
        config.rightForeArmAngle = -48.0
        # The horizontal leveling angle we fine-tuned
        config.jebenaAngle = 35.0
        config.coffeeFlow = True
        config.headAngle = -15.0
    elif 51 <= t < 57:
        ef = ss((t - 51) / 4.0)
        config.rightArmAngle = lerp(-52, -50, ef)
        config.rightForeArmAngle = lerp(-48, -80, ef)
        config.leftArmAngle = lerp(35, -60, ef)
        config.leftForeArmAngle = lerp(18, -70, ef)
        config.coffeeFlow = False
        config.headAngle = -10
    elif 57 <= t < 85:
        cycle_dur = 5.6
        cur_idx = min(4, int((t - 57) / cycle_dur))
        sub_t = (t - 57) % cycle_dur
        config.servedCupsCount = cur_idx 
        target_x = config.NB_COORDS[cur_idx][0] + 25
        config.rightArmAngle = -50
        config.rightForeArmAngle = -80
        config.leftArmAngle = -60
        config.leftForeArmAngle = -70
        config.headAngle = -10
        if sub_t < 2.5: 
            prog = ss(sub_t / 2.5)
            config.woman_cur_x = lerp(config.WOMAN_BASE_X, target_x, prog)
            config.holdingCup = True
        elif sub_t < 3.8: 
            config.woman_cur_x = target_x
            config.holdingCup = False if sub_t > 3.2 else True
        else: 
            prog = ss((sub_t - 3.8) / 1.8)
            config.woman_cur_x = lerp(target_x, config.WOMAN_BASE_X, prog)
            config.holdingCup = False
            if sub_t > 5.0:
                config.servedCupsCount = min(5, cur_idx + 1)
    elif t >= 85:
        config.servedCupsCount = 5
        config.rightArmAngle = -15
        config.rightForeArmAngle = -10
        config.leftArmAngle = 35
        config.leftForeArmAngle = 18