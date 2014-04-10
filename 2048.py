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

class Map:
    data = None
    height = None
    width = None

    def __init__(self, h, w, start_count):
        if h == 0 or w == 0:
            raise Exception("Wrong dimensions.")

        self.height = h
        self.width = w

        self.data = [[0 for i in range(self.width)] for j in range(self.height)]

        for i in xrange(min(start_count, self.height*self.width)):
            x, y = self.get_random_empty()
            self.data[x][y] = 2

    def get_random_empty(self):
        squares = self.height*self.width
        start_n = n = randint(0, squares-1)
        k = 0
        while True:
            i = k/self.width
            j = k%self.width
            if self.data[i][j] == 0:
                if n == 0:
                    return [i, j]
                n -= 1
            k +=1
            if k == squares:
                if n == start_n: #no empty
                    return None
                k = 0

    def set_cell(self, x, y, value):
        self.data[x][y] = value

    def print_map(self, nl=True):
        print "+-----"*self.width + "+"
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.data[i][j] == 0:
                    print "|    ",
                else:
                    print "|%4d"%(self.data[i][j]),
            print "|"
            print "+-----"*self.width + "+"
        if nl:
            print ""

    def is_valid(self, x, y):
        return x >= 0 and x < self.height and y >= 0 and y < self.width

    def get_movements(self):
        return {'l': [[x, y] for x in xrange(0, self.height) for y in xrange(0, self.width, 1)],
                'r': [[x, y] for x in xrange(0, self.height) for y in xrange(self.width-1, -1, -1)],
                'd': [[y, x] for x in xrange(0, self.width) for y in xrange(self.height-1, -1, -1)],
                'u': [[y, x] for x in xrange(0, self.width) for y in xrange(0, self.height, 1)]}

    def move(self, direction='l'):
        di, dj = {'l': [0, -1], 'r': [0, +1], 'd': [1, 0], 'u':[-1, 0]}[direction]
        mov = self.get_movements()[direction]

        merged = {}
        m = self.data

        for i, j in mov:
            while self.is_valid(i+di, j+dj) and m[i+di][j+dj] == 0:
                m[i+di][j+dj] = m[i][j]
                m[i][j] = 0
                j += dj
                i += di
            if self.is_valid(i+di, j+dj) and m[i+di][j+dj] == m[i][j] and \
                    not merged.get((i+di, j+dj)):
                merged[(i+di, j+dj)] = True
                m[i+di][j+dj] *= 2
                m[i][j] = 0

        self.data = m

def play(height=4, width=4, init=2):
    getch = _Getch()
    keys = {"j":"d", "h":"l", "k":"r", "u":"u"}
    m = Map(height, width, init)
    while True:
        m.print_map()
        char = getch()
        if char == "q":
            break
        if char not in keys:
            print "Unknown char."
            continue
        m.move(keys[char])

        p = m.get_random_empty()
        if p:
            m.set_cell(p[0], p[1], 2)
        else:
            print "You loose"
            break

