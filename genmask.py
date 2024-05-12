import os
from random import random
from math import sin,cos,pi


def update_output(output, borders):
    work = []
    x = 0
    y = 0
    for elem in output:
        out_val = elem
        for b in borders:
            if b['x'] == x and b['y'] == y:
                out_val = next_value(b['pix'])
        work.append(out_val)
        x += 1
        if x == 40:
            x = 0
            y += 1
    return work


def detect_borders(output):
    total_borders = []
    for y in range(25):
        inside = False
        prevInside= False
        prevX = -1
        borders = []
        for x in range(40):
            pix = output[y*40+x]
            if not inside and pix == 0:
                inside = True
                if not prevInside:
                    borders.append(prevX)
                    prevInside = True
            elif inside and pix != 0:
                inside = False
                if prevInside:
                    prevInside = False
                    borders.append(x)
            prevX = x
        total_borders.append(borders)

    borders = []
    for y in range(25):
        for x in range(40):
            if x in total_borders[y]:
                val_out = output[y*40+x]
                borders.append({'x':x, 'y':y, 'pix':val_out})

    return borders


def classification(c1, c2, pix):
    # 12 = bits 0, 1, 2 et 3
    # 34
    out = 15
    if pix == [0, 0, 0, 0, 0, 0, 0, 0]:
        out = 0b00001111
    else:
        if pix[0] & 240:
            out -= 1
        if pix[0] & 15:
            out -= 2
        if pix[4] & 240:
            out -= 4
        if pix[4] & 15:
            out -= 8
    return out


def next_value(pix):
    nb_pixels = 0
    for i in [1,2,4,8]:
        if pix & i:
            nb_pixels += 1
    target_pixels = nb_pixels - 1
    next_pix = '0000'
    val_next = 0
    while next_pix.count('1') != target_pixels:
        next_pix = ''
        val_next = 0
        val_bit = 1
        for i in range(4):
            if random() <= 0.5:
                next_pix += '1'
                val_next += val_bit
            else:
                next_pix += '0'
            val_bit = val_bit *2

    return val_next


def print_hires(hires):
    os.system('clear')
    for y in range(25):
        for x in range(40):
            val_out = hires[y*40+x]
            desc = "0123456789ABCDEF"[val_out]
            if val_out == 0:
                print('.', end='')
            else:
                print(desc, end='')
        print()


hin = open('mask-logo.kla', 'rb')

load = hin.read(2)
hires = []
for i in range(8000):
    hires.append(hin.read(1))
color1 = []
for i in range(1000):
    color1.append(hin.read(1))
color2 = []
for i in range(1000):
    color2.append(hin.read(1))
hin.close()

output = []
nb_out = 0
for y in range(25):
    for x in range(40):
        col1 = color1[40*y+x][0]
        col2 = color2[40*y+x][0]
        pixels = []
        all255 = True
        allAA = True
        all55 = True
        for pix in range(8):
            pix = hires[320*y+8*x+pix][0]
            pixels.append(pix)
            if pix != 255:
                all255 = False
            if pix != 170:
                allAA = False
            if pix != 85:
                all55 = False
        if (col2 % 16 == 11 and all255) or (col1 % 16 == 11 and allAA) or \
           (col1 & 240 == 11 * 16 and all55):
            val_out = 0
        else:
            val_out = classification(col1, col2, pixels)

        output.append(val_out)
        desc = '.'
        if val_out != 0:
            desc = "0123456789ABCDEF"[val_out]
            nb_out += 1
        print(desc, end='')
    print('')

hout = open('mask.bin', 'wb')
for elem in output:
    hout.write(elem.to_bytes(1, 'little'))
hout.close()
print('total modifiable = %d' % nb_out)

all_borders = []
borders = detect_borders(output)
all_borders.append(borders)
print(len(borders))

while len(borders) != 0:
    output = update_output(output, borders)
    borders = detect_borders(output)
    all_borders.append(borders)
    print(len(borders))

output = update_output(output, borders)
print_hires(output)

# write results

written = 0
framepos = 0
frames = []


hout = open('anim.bin', 'wb')
nb_borders = len(all_borders)
for i in range(nb_borders):
    print('process output %d length %d' % (i, len(all_borders[nb_borders - i - 1])))
    not_zero = False
    for elem in all_borders[nb_borders - i - 1]:
        not_zero = True
        x = elem['x']
        y = elem['y']
        pix = elem['pix'] * 8
        target = 0x6000 + 320*y + x*8
        target_l = target & 255
        target_h = int(target / 256)
        hout.write(pix.to_bytes(1, 'big'))
        hout.write(target_l.to_bytes(1, 'big'))
        hout.write(target_h.to_bytes(1, 'big'))
        written += 3
    if not_zero:
        hout.write((0).to_bytes(1, 'big'))
        written += 1
        frames.append(framepos)
        framepos += written
        written = 0
        

print('first frames = %d' % len(frames))

for i in range(nb_borders):
    print('process output %d length %d' % (i, len(all_borders[i])))

    # remove old values

    if i > 0:
        for elem in all_borders[i - 1]:
            x = elem['x']
            y = elem['y']
            pix = 16*8
            target = 0x6000 + 320*y + x*8
            target_l = target & 255
            target_h = int(target / 256)
            hout.write(pix.to_bytes(1, 'big'))
            hout.write(target_l.to_bytes(1, 'big'))
            hout.write(target_h.to_bytes(1, 'big'))
            written += 3
    # plot new values
    not_zero = False
    for elem in all_borders[i]:
        not_zero = True
        x = elem['x']
        y = elem['y']
        pix = elem['pix'] * 8
        target = 0x6000 + 320*y + x*8
        target_l = target & 255
        target_h = int(target / 256)
        hout.write(pix.to_bytes(1, 'big'))
        hout.write(target_l.to_bytes(1, 'big'))
        hout.write(target_h.to_bytes(1, 'big'))
        written += 3
    if not_zero:
        hout.write((0).to_bytes(1, 'big'))
        written += 1
        frames.append(framepos)
        framepos += written
        written = 0

hout.write((0).to_bytes(1, 'big'))
hout.close()
print('total frames = %d' % nb_borders)
print(frames)

hout = open('framesL.bin', 'wb')
for pos in frames:
    posL = pos & 255
    hout.write(posL.to_bytes(1, 'big'))
hout.close()

hout = open('framesH.bin', 'wb')
for pos in frames:
    posL = int(pos / 256) + 16 + 11
    hout.write(posL.to_bytes(1, 'big'))
hout.close()

print('total frames = %d' % len(frames))

# gen anim

anim = [0]
delays = [0]
for i in range(256):
    pic = int(47 + 47*cos(pi+i*pi/256))
    if pic > 93:
        pic = 93
        print('***max')
    
    last_pos = len(anim) - 1
    if pic == anim[last_pos]:
        delays[last_pos] += 1
    else:
        if abs(pic-anim[last_pos]) > 1:
            input('delta !', pic)
        
        anim.append(pic)
        delays.append(0)

print(anim)
print(delays)
hout = open('anim_frames.bin', 'wb')
for i in range(len(anim)):
    hout.write(anim[i].to_bytes(1, 'big'))
    ndelay = delays[i]
    if ndelay < 0:
        ndelay = 8
    hout.write(ndelay.to_bytes(1, 'big'))
for i in range(len(anim)):
    hout.write(anim[i].to_bytes(1, 'big'))
    ndelay = 6 - delays[i]
    if ndelay < 0:
        ndelay = 5
    hout.write(ndelay.to_bytes(1, 'big'))
hout.write((128).to_bytes(1, 'big'))
hout.close()

