from random import random
from math import pi, sin, cos


def gen_vert_transition():
    coords = []
    for y in range(8):
        for x in range(72):
            coords.append([x, y])

    return coords


def gen_boom_transition():
    coords = []
    pool = []
    for y in range(8):
        zpool = []
        for x in range(72):
            zpool.append(1)
        pool.append(zpool)

    for j in range(64):
        r = 0.1 + j / 64
        for i in range(256):
            x = int(35.5 + 36 * r * cos(2*pi*i/256))
            y = int(3.5 + 4 * r * sin(2*pi*i/256))
            if x >= 0 and x <= 71 and y >= 0 and y <= 7 and pool[y][x] == 1:
                pool[y][x] = 0
                coords.append([x, y])
    for y in range(8):
        for x in range(72):
            if pool[y][x] == 1:
                coords.append([x, y])
                pool[y][x] = 0

    return coords




def gen_rain_transition():
    coords = []
    pool = []
    for y in range(8):
        for x in range(72):
            pool.append([x, y])
    runners = []
    posx = []
    
    for x in range(72):
        posx.append(x)

    for x in range(72):
        pos = int(random() * len(posx))
        runners.append([posx[pos], -int(7 * random())])
        del posx[pos]

    nb_tot = 8 * 72
    while nb_tot != 0:
        for pos_runner in range(len(runners)):
            x = runners[pos_runner][0]
            y = runners[pos_runner][1]
            if y >= 0 and y <= 7:
                nb_tot -= 1
                coords.append([x, y])
            runners[pos_runner][1] += 1

    return coords


def gen_random_transition():
    coords = []
    pool = []
    for y in range(8):
        for x in range(72):
            pool.append([x, y])
    while len(pool) != 0:
        pos = int(random() * len(pool))
        coords.append(pool[pos])
        del pool[pos]
    return coords


def gen_arrow_transition():
    coords = []
    nb_tot = 8*72
    runners = [[-3, 0], [-2, 1], [-1, 2], [0, 3], [0, 4],
               [-1, 5], [-2, 6], [-3, 7]]
    while nb_tot != 0:
        for runner_pos in range(len(runners)):
            x = runners[runner_pos][0]
            y = runners[runner_pos][1]
            if x >= 0 and x<= 71 and y >= 0 and y <= 8:
                nb_tot -= 1
                coords.append([x, y])
            runners[runner_pos][0] += 1
    return coords


def int2bin(valeur):
    v =''
    for i in [128, 64, 32, 16, 8, 4, 2, 1]:
        if (valeur & i) != 0:
            v += '#'
        else:
            v += '.'
    return v


def gen_lines(texte, font):
    lines = ['', '', '', '', '', '', '', '']
    for i in texte:
        car = ord(i)
        if car >= 64:
            car = car - 64
        pos = car * 8
        for line in range(8):
            lines[line] += int2bin(font[pos + line])
    return lines


def print_lines(lines):
    for line in range(8):
        print(lines[line])


hin = open('c64.bin', 'rb')
font = []
for i in range(2048):
    value = hin.read(1)
    font.append(int.from_bytes(value, "big"))
hin.close()

textes = ['         ',
          '[alien]',
          '[blien]',
          '[alien]',
          '[byg]',
          ' @X 2024 ',
          'VARIATION',
          'AROUND A ',
          '<L O G O>',
          '         ',
          ' ARTWORK ',
          ' BY NYKE ',
          ' TUNE BY ',
          ' MAGNAR! ',
          ' CODE BY ',
          'PAPAPOWER',
          '         ',
          '[pac]',
          'GREETINGS',
          'FLYING TO',
          'BUSYSOFT,',
          'ROLE, G*P',
          ' CENSOR, ',
          'HOKUTO F.',
          ' LAXITY, ',
          'FAIRLIGHT',
          'F4CG,TRSI',
          ' REALITY,',
          'XINY 6581',
          '[aliens2]',
          '[aliens2b]',
          '[aliens2]',
          'TRIAD,TLF',
          ' EXCESS, ',
          ' COSINE, ',
          'ONSLAUGHT',
          ' OXYRON, ',
          ' HOAXERS,',
          'ATLANTIS,',
          ' ARSENIC,',
          'SONIC,LFT',
          '  PADUA, ',
          '[k7]',
          '  KRILL, ',
          '  CUPID, ',
          '  SHINE, ',
          '  PLUSH, ',
          'SOLUTION,',
          ' LUKHASH ',
          '  XENON, ',
          ' BLAZON, ',
          'AND YOU !',  
          '         ']

pac = [
        '......####.................#########.................#######............',
        '....#######...............###########..............##########...........',
        '...#########.............#####..##..##............####..##..##..........',
        '...######.......##.......#####.###.###............####.###.###..........',
        '...####........####......#############............############..........',
        '...#######......##.......#############............############..........',
        '....#######..............####.####.###............############..........',
        '......####................##...##..##..............##..##..##...........'
       ]

byg = [
        '.............######......###....##......########...........##...........',
        '............##....##......###..##.....##.......##.........##............',
        '...........##.....#........###.......##..................##.............',
        '...........##....####.......##......##..................##..............',
        '..........##........##.....##.....##....#####..........##...............',
        '.........##........##.....##.....##.......##............................',
        '........##........##.....##.....##.......##..........##.................',
        '........##########......##.......########...........##..................'
       ]

k7 = [
        '......................#.........#......###.....##...........#####.......',
        '...##############....##.........##.....###...#.###.........#.....#......',
        '...#............#.......#######........###...#.###........#.......#.....',
        '...#..#......#..#......#...#...#.......###.....###........#.......#.....',
        '...#............#......####.####.......###########........#.#####.#.....',
        '...#..########..#.......#######........###########.........#.#.#.#......',
        '...#.##########.#....##.#..#..#.##.....###########.........#.....#......',
        '...##############.....#.........#......###########..........#####.......',
    ]

aliens2 = [
        '...#...#............###..........##...##.......###........###...###.....',
        '....###.........#..#####..#.......#####.......#####.......#..#.#..#.....',
        '...#.#.#........###..#..###......#.###.#.....#.###.#........#####.......',
        '..##.#.##........###.##.##.......#.###.#.....#.###.#......#########.....',
        '..#######........##..#..##........##.##.......#####.......##.###.##.....',
        '...#####.........#########.......#######....#..#.#..#....#.###.###.#....',
        '..#.#.#.#........#.#.#.#.#.......#.#.#.#.....##.#.##.....#..#####..#....',
        '...................................#.#.....................##...##......'
    ]

aliens2b = [
        '.......#............###..........##...##................####.....####...',
        '..#####............#####..........#####........###..........#...#.......',
        '...#.#.#.........##..#..##.......#.###.#......#####......#..#####..#....',
        '..##.#.##.......###.##.####......#.###.#.....#.###.#.....###########....',
        '..#######......#.##..#..##.#......##.##......#.###.#......##.###.##.....',
        '...#####.........#########.......#######......#####........###.###......',
        '..#.#.#.#........#.#.#.#.#.......#.#.#.#....#..#.#..#.......#####.......',
        '...................................#.#.......##.#.##.......##...##......'
    ]


alien0 = '..#.....#...'
alien1 = '...#...#....'
alien2 = '..#######...'
alien3 = '.##.###.##..'
alien4 = '###########.'
alien5 = '#.#######.#.'
alien6 = '#.#.....#.#.'
alien7 = '...##.##....'

alien = [alien0 * 6,
         alien1 * 6,
         alien2 * 6,
         alien3 * 6,
         alien4 * 6,
         alien5 * 6,
         alien6 * 6,
         alien7 * 6]

blien0 = '..#.....#...'
blien1 = '...#...#....'
blien2 = '#.#######.#.'
blien3 = '###.###.###.'
blien4 = '.#########..'
blien5 = '..#######...'
blien6 = '..#.....#...'
blien7 = '.#.......#..'

blien = [blien0 * 6,
         blien1 * 6,
         blien2 * 6,
         blien3 * 6,
         blien4 * 6,
         blien5 * 6,
         blien6 * 6,
         blien7 * 6]

tot_lines = []
for texte in textes:
    if texte == '[alien]':
        lines = alien
    elif texte == '[blien]':
        lines = blien
    elif texte == '[pac]':
        lines = pac
    elif texte == '[byg]':
        lines = byg
    elif texte == '[k7]':
        lines = k7
    elif texte == '[aliens2]':
        lines = aliens2
    elif texte == '[aliens2b]':
        lines = aliens2b
    else:    
        lines = gen_lines(texte, font)
    tot_lines.append(lines)
    print_lines(lines)

# 6 sprites horizontally = 144 pixels, 2 pixels per source pixel = 9 chars
# = 72 x 2 pixels
# height = 16 pixels for 8 positions
# we're going to store directly the write offset + on the high bits the X position
# in high byte = 4 possibilities 11000000, 00110000, 00001100, 00000011
# write will be using XOR

offsets = []
for x in range(72):
    for y in range(8):
        sprite = int(x / 12)
        reste_x = x % 12
        octet = int(reste_x / 4)
        pixels_x = reste_x % 4
        rang_y = int(y / 4)
        reste_y = y % 4
        offset = sprite * 64 + y * 6 + octet
        indic_x = pixels_x << 6
        encoded = offset + indic_x * 256
        if encoded & 255 == 255:
            input('255!')
        offsets.append(encoded)
print(offsets)
print(len(offsets))

flux = []
flux.append(255+ 256 * 254)

start = []
for y in range(8):
    line = ''
    for x in range(72):
        line += '.'
    start.append(line)

transitions = [gen_random_transition(), gen_boom_transition(), 
               gen_vert_transition(), gen_vert_transition(),
               gen_rain_transition(), gen_boom_transition(),
               gen_random_transition(), gen_arrow_transition(),
               gen_random_transition(), gen_boom_transition(),
               gen_random_transition(), gen_rain_transition(),
               gen_arrow_transition(), gen_arrow_transition(),
               gen_random_transition(), gen_rain_transition(),
               gen_arrow_transition(),  gen_boom_transition(),
               gen_random_transition(), gen_rain_transition(),
               gen_arrow_transition(), gen_boom_transition(),
               gen_rain_transition(), gen_random_transition()]
frames = len(tot_lines)

while len(transitions) != frames:
    alea = int(random() * 5)
    rand = gen_random_transition()
    if alea == 0:
        rand = gen_rain_transition()
    elif alea == 1:
        rand = gen_vert_transition()
    elif alea == 2:
        rand = gen_arrow_transition()
    elif alea == 3:
        rand = gen_boom_transition()
    transitions.append(rand)

print('frames = %d' % frames)
for frame in range(frames):
    for pos in transitions[frame]:
        x = pos[0]
        y = pos[1]
        line_test = tot_lines[frame][y]
        line_origin = start[y]
        if line_test[x] != line_origin[x]:
            start[y] = line_origin[:x] + line_test[x] + line_origin[x + 1:]
            flux.append(offsets[x * 8 + y])
    for y in range(8):
        print(start[y])
    print('--')
    flux.append(255+ 256 * 64)

# FFFF to stop
flux.append(65535)

print(len(flux))
hout = open('flux.bin', 'wb')
for off in flux:
    off_low = off & 255
    off_high = off >> 8
    hout.write(off_low.to_bytes(1, byteorder='big'))
    hout.write(off_high.to_bytes(1, byteorder='big'))
hout.close()

hout = open('offsets.bin', 'wb')
for off in offsets:
    off_low = off & 255
    off_high = off >> 8
    hout.write(off_low.to_bytes(1, byteorder='big'))
    hout.write(off_high.to_bytes(1, byteorder='big'))
hout.close()

