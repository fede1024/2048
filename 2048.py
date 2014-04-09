import sys
from random import randint

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def gen_map(n):
    m = [[0 for i in range(4)] for j in range(4)]

    for i in xrange(n):
        m[randint(0, 3)][randint(0, 3)] = 2

    return m

def print_map(m, nl=True):
    print "+-----+-----+-----+-----+"
    for i in xrange(4):
        for j in xrange(4):
            if m[i][j] == 0:
                print "|    ",
            else:
                print "|%4d"%(m[i][j]),
        print "|"
        print "+-----+-----+-----+-----+"
    if nl:
        print ""

def inside_map(x, y):
    return x >= 0 and x < 4 and y >= 0 and y < 4

def get_movements(size):
    return {'l': [[x, y] for x in xrange(0, 4) for y in xrange(0, 4, 1)],
            'r': [[x, y] for x in xrange(0, 4) for y in xrange(3, -1, -1)],
            'd': [[y, x] for x in xrange(0, 4) for y in xrange(3, -1, -1)],
            'u': [[y, x] for x in xrange(0, 4) for y in xrange(0, 4, 1)]}

def move(m, direction='l'):
    di, dj = {'l': [0, -1], 'r': [0, +1], 'd': [1, 0], 'u':[-1, 0]}[direction]
    mov = get_movements(4)[direction]

    merged = {}

    for i, j in mov:
        while inside_map(i+di, j+dj) and m[i+di][j+dj] == 0:
            m[i+di][j+dj] = m[i][j]
            m[i][j] = 0
            j += dj
            i += di
        if inside_map(i+di, j+dj) and m[i+di][j+dj] == m[i][j] and \
           not merged.get((i+di, j+dj)):
            merged[(i+di, j+dj)] = 1
            m[i+di][j+dj] *= 2
            m[i][j] = 0

def random_empty(m):
    n = randint(0, 15)
    k = 0
    while True:
        i = k%4
        j = k/4
        if m[i][j] == 0:
            if n == 0:
                return [i, j]
            n -= 1
        k = (k+1)%16

def play():
    getch = _Getch()
    keys = {"j":"d", "h":"l", "k":"r", "u":"u"}
    m = gen_map(10)
    while True:
        print_map(m)
        char = getch()
        if char == "q":
            break
        if char not in keys:
            print "Unknown char."
            continue
        move(m, keys[char])

        p = random_empty(m)
        if p:
            m[p[0]][p[1]] = 2
        else:
            print "You loose"
            break

