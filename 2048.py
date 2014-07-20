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

    def __init__(self, h, w, start_count, copy_from=None):
        if copy_from:
            self.height = copy_from.height
            self.width = copy_from.width
            self.data = [row[:] for row in copy_from.data]
            self.movements = copy_from.movements
            return

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
        return Map(0, 0, 0, copy_from=self)

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
    print "Press h for left, k for right, j for down and u for up."
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

def heur_emptys(map):
    return len(map.get_empty_cells())

def heur_squared(map):
    s= 0
    for i in xrange(map.height):
        for j in xrange(map.width):
            v = map.data[i][j]
            s += v*v
    return s

def minimax(map, depth, my_turn, heur):
    empty_cells = map.get_empty_cells()
    stop_treshold = 0# if len(empty_cells) >= 4 else -2

    if depth <= stop_treshold:
        return [heur(map), None]

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
            n = minimax(tmp, depth-1, not my_turn, heur)[0]
            if v == None or n > v: #MAX
                v = n
                best = mov
        if not change:
            return [heur(map), None]
    else:
        moves = [[x, y, 2] for x, y in empty_cells] + [[x, y, 4] for x, y in empty_cells]
        for x, y, val in moves:
            tmp = map
            tmp.set_cell(x, y, val)
            n = minimax(tmp, depth-1, not my_turn, heur)[0]
            tmp.set_cell(x, y, 0)
            if v == None or n < v: #MIN
                v = n
                best = [x, y]

    return v, best

def expectimax(map, depth, my_turn, heur):
    empty_cells = map.get_empty_cells()
    stop_treshold = 0# if len(empty_cells) >= 4 else -2

    if depth <= stop_treshold:
        return [heur(map), None]

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
            n = expectimax(tmp, depth-1, not my_turn, heur)[0]
            if v == None or n > v: #MAX
                v = n
                best = mov
        if not change:
            return [heur(map), None]
    else:
        moves = [[x, y, 2] for x, y in empty_cells] + [[x, y, 4] for x, y in empty_cells]
        moves_no = float(len(moves))
        best = None
        n = 0
        for x, y, val in moves:
            tmp = map
            tmp.set_cell(x, y, val)
            n += expectimax(tmp, depth-1, not my_turn, heur)[0]/moves_no
            tmp.set_cell(x, y, 0)
        v = n

    return v, best

def AI(height=4, width=4, init=2, interactive=False, depth=4, heur=heur_emptys):
    start_time = time.time()
    getch = _Getch()
    m = Map(height, width, init)
    moves = 0
    while True:
        if interactive:
            m.print_map()
        #r = minimax(m, depth, True, heur)
        r = minimax(m, depth, True, heur)
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
            return p, moves, best_tile, t, m

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

def sign(n):
    return 1 if n >= 0 else -1

def heur_monoton(map):
    transp = [[r[i] for r in map.data] for i in xrange(len(map.data[0]))]

    def get_score(data):
        score = 0
        for i in xrange(map.height):
            d_p = data[i][1] - data[i][0]
            for j in xrange(2, map.width):
                d = data[i][j] - data[i][j-1]
                if data[i][j] == 0:
                    score += 1.5
                if not d or sign(d) == sign(d_p):
                    score +=1
                else:
                    score -= 1
                d_p = d
        return score

    return get_score(map.data) + get_score(transp)

def heur_top(map):
    last = map.width - 1
    transp = [[r[i] for r in map.data] for i in xrange(len(map.data[0]))]

    def get_score(data):
        score = 0
        for col in data:
            m = max(col)
            if col[0] == m or col[last] == m:
                score += 1
        return score

    return len(map.get_empty_cells()) + get_score(map.data) + get_score(transp)

def heur_top2(map):
    last = map.width - 1
    transp = [[r[i] for r in map.data] for i in xrange(len(map.data[0]))]

    def get_score(data):
        score = 0
        for col in data:
            m = max(col)
            if col[0] == m or col[last] == m:
                score += m*m
        return score

    return heur_squared(map) + get_score(map.data) + get_score(transp)
    #print heur_squared(map), get_score(map.data), get_score(transp)

if __name__ == "__main__":
     #play(4, 4)
     #AI(4, 4, heur=heur_2)
     p1 = [AI(4, 4, depth=4, heur=heur_emptys) for x in xrange(10)]
     p2 = [AI(4, 4, depth=4, heur=heur_squared) for x in xrange(10)]
     p3 = [AI(4, 4, depth=4, heur=heur_monoton) for x in xrange(10)]
     p4 = [AI(4, 4, depth=4, heur=heur_top2) for x in xrange(10)]
     print sum(x[0] for x in p1)/10.0
     print sum(x[0] for x in p2)/10.0
     print sum(x[0] for x in p3)/10.0
     print sum(x[0] for x in p4)/10.0
     #print "ciao"

#  EURISTIC      MINIM   EXPEC
# heur_emptys   1441.0  1161.4
# heur_squared  1158.0  1292.2
# heur_monoton  1765.8  1484.0
# heur_top2      950.2  1232.8


#  Done, 2982 points in 1349 moves (best tile: 2048).
#  Time elapsed: 43.01 seconds
#  +-----+-----+-----+-----+
#  |2048 |   4 |   2 |  16 |
#  +-----+-----+-----+-----+
#  |   4 | 256 |   8 | 512 |
#  +-----+-----+-----+-----+
#  |  32 |   4 |  16 |   4 |
#  +-----+-----+-----+-----+
#  |   8 |   2 |  64 |   2 |
#  +-----+-----+-----+-----+

#  Done, 4074 points in 1849 moves (best tile: 2048).
#  Time elapsed: 1671.02 seconds
#  +-----+-----+-----+-----+
#  |   2 |  16 | 512 |  32 |
#  +-----+-----+-----+-----+
#  | 256 | 128 |  16 |   8 |
#  +-----+-----+-----+-----+
#  |1024 |  16 |   4 |   2 |
#  +-----+-----+-----+-----+
#  |2048 |   4 |   2 |   4 |
#  +-----+-----+-----+-----+

