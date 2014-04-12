import sys
from random import randint, random
import copy, time

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

        self.movements = self.generate_movements()

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

    def get_empty_cells(self):
        cells = []
        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.data[i][j] == 0:
                    cells.append([i, j])
        return cells

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

    def generate_movements(self):
        return {'l': [[x, y] for x in xrange(0, self.height) for y in xrange(0, self.width, 1)],
                'r': [[x, y] for x in xrange(0, self.height) for y in xrange(self.width-1, -1, -1)],
                'd': [[y, x] for x in xrange(0, self.width) for y in xrange(self.height-1, -1, -1)],
                'u': [[y, x] for x in xrange(0, self.width) for y in xrange(0, self.height, 1)]}

    def move(self, direction='l'):
        di, dj = {'l': [0, -1], 'r': [0, +1], 'd': [1, 0], 'u':[-1, 0]}[direction]
        mov = self.movements[direction]

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

    def get_copy(self):
        return copy.deepcopy(self)

    def equal(self, map):
        if self.height != map.height or self.width != map.width:
            return False

        for i in xrange(self.height):
            for j in xrange(self.width):
                if self.data[i][j] != map.data[i][j]:
                    return False

        return True

def new_cell_value():
    if random() > 0.1:
        return 2
    else:
        return 4

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
            m.set_cell(p[0], p[1], new_cell_value())
        else:
            print "You loose"
            break

def heur_2(map):
    return len(map.get_empty_cells())

def heur_1(map):
    s= 0
    for i in xrange(map.height):
        for j in xrange(map.width):
            v = map.data[i][j]
            s += v*v
    return s

def minimax(map, depth, my_turn):
    empty_cells = map.get_empty_cells()
    stop_treshold = 0# if len(empty_cells) >= 4 else -2

    if depth <= stop_treshold:
        #print ">>>", depth, stop_treshold, len(empty_cells)
        return [heur_1(map), None]

    v = None
    best = None

    if my_turn:
        change = None
        for mov in ['l', 'r', 'u', 'd']:
            tmp = map.get_copy()
            tmp.move(mov)
            if map.equal(tmp):
                continue
            change = True
            n = minimax(tmp, depth-1, not my_turn)[0]
            #print "    "*(4-depth), mov, n, heur_1(tmp)
            if v == None or n > v: #MAX
                v = n
                best = mov
        if not change:
            #print ">>"+"    "*(4-depth), heur_1(map)
            #print "UPPA", depth, stop_treshold, len(empty_cells)
            return [heur_1(map), None]
    else:
        #empty_cells = map.get_empty_cells()
        moves = [[x, y, 2] for x, y in empty_cells] + [[x, y, 4] for x, y in empty_cells]
        for x, y, val in moves:
            tmp = map.get_copy()
            tmp.set_cell(x, y, val)
            n = minimax(tmp, depth-1, not my_turn)[0]
            #print "    "*(4-depth), [x, y], n, heur_1(tmp)
            #print ".   "*(4-depth), v, best
            if v == None or n < v: #MIN
                #print "u>  "+"    "*(3-depth), n, [x, y]
                v = n
                best = [x, y]

    #print "+>  "+"    "*(3-depth), v, best
    return v, best

def AI(height=4, width=4, init=2, interactive=False, depth=4):
    start_time = time.time()
    getch = _Getch()
    m = Map(height, width, init)
    moves = 0
    while True:
        if interactive:
            m.print_map()
        r = minimax(m, depth, True)
        if not r[1] or moves % 10 == 0:
            p = 0
            best_tile = 0
            for i in xrange(m.height):
                for j in xrange(m.width):
                    p += m.data[i][j]
                    best_tile = max(best_tile, m.data[i][j])
            t = round(time.time() - start_time, 2)
            print "Done, %d points in %d moves (best tile: %d)."%(p, moves, best_tile)
            print "Time elapsed:", t, "seconds"
            m.print_map()
        if not r[1]:
            return p, moves, best_tile, t

        if interactive:
            print "Next move: ", r
            char = getch()
        else:
            char = " "

        if char == "q":
            break
        elif char == " ":
            m.move(r[1])
            moves += 1
        else:
            print "Unknown char."
            continue

        p = m.get_random_empty()
        if p:
            m.set_cell(p[0], p[1], new_cell_value())
        else:
            print "You loose"
            break

if __name__ == "__main__":
    AI(3, 3, depth=4)

