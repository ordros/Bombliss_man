import sys
from itertools import chain
import time
from config_bombliss import TETRIMINOS

class ThinkBombliss:
    def __init__(self, boardsize):
        self.boardsize_x = boardsize[0]
        self.boardsize_y = boardsize[1]

    def fall(self, board, mino, xpos):
        if xpos + len(mino[0]) > len(board[0]):
            raise Exceptions
        for ypos in range(0, len(board)):
            for y in range(0, len(mino)):
                for x in range(0, len(mino[0])):
                    if ypos+len(mino) > self.boardsize_y :
                        #print "Over."
                        return ypos-1
                    if board[ypos+y][xpos+x] and mino[y][x] :
                        #print "Collision.",x,y,xpos,ypos
                        return ypos-1
        return ypos

    def make_frame(self, board):
        board_w = []
        board_w.append([1 for x in xrange(len(board[0])+2)])
        for i in board:
            board_w.append([1] + i + [1])
        board_w.append([1 for x in xrange(len(board[0])+2)])

        return board_w

    def eval_space4(self, board, mino, px, py):
        one_sum = 0
        b = self.compose_mino(board, mino, px, py)

        #for i in range(py+2, len(b)):
        #    one_sum += sum(b[i])
        #return float(one_sum) #/ ((len(board)-py)*len(board[0]))

        return sum(mino[len(mino)-1])

    def eval_space3(self, board, mino, px, py):
        b = self.compose_mino(board, mino, px, py)
        #for i in b: print i

        board_w = self.make_frame(b)
        cnt = 0
        size = (len(mino)+1) * (len(mino[0]))

        for y in xrange(py, py+len(mino)+1):
            for x in xrange(px, px+len(mino[0])):
                if not board_w[y][x] : cnt += 1
        return cnt

    # refactoring
    def eval_space2(self, board, mino, px, py):
        cnt = 0
        penalty_adjacent = 0
        b = self.compose_mino(board, mino, px, py)
        board_w = self.make_frame(b)
        for y in xrange(1, len(board)+1):
            for x in xrange(1, len(board[0])+1):
                above = board_w[y+1][x]
                under = board_w[y-1][x]
                left = board_w[y][x-1]
                right = board_w[y][x+1]
                if board_w[y][x] == 0 :
                    if above * under * left * right :
                        cnt += 1
                        continue
                        #board_w[y][x] = 2
                    if above * under * left :
                        cnt += 1
                        continue
                        #board_w[y][x] = 2
                    if above * under * right :
                        cnt += 1
                        continue
                        #board_w[y][x] = 2
                    if above * right * left :
                        cnt += 1
                        continue
                        #board_w[y][x] = 2
                    if right * under * left :
                        cnt += 1
                        continue
                        #board_w[y][x] = 2
                    if under * above :
                        cnt += 1
                        continue
#        for y in xrange(1, len(board)+1):
#            for x in xrange(1, len(board[0])+1):
#                if board_w[y][x] == 2 :
#                    if board_w[y+1][x] == 2 or board_w[y-1][x] == 2 or board_w[y][x+1] == 2 or board_w[y][x-1] == 2 : penalty_adjacent += 1

        #for w in board_w:
        #    print w
        return ((len(board)+1) * (len(board[0])+1)) - cnt

    def eval_space(self, board):
        match_blocks = 0
        matchs = 0
        ones = 0

        for block in ILLEGAL_BLOCK:
            for y in range(0, len(board)-len(block)+1):
                for x in range(0, len(board[0])-len(block[0])+1):
                    for by in range(0, len(block)):
                        for bx in range(0, len(block[0])):
                            if board[y+by][x+bx] == block[by][bx] :
                                matchs += 1
                            ones += block[by][bx]

                    if matchs == ones :
                        match_blocks += 1
                    matchs = 0
                    ones = 0
        return match_blocks

    # refactor
    def compose_mino(self, board, mino, px, py):
        b = [[0 for i in xrange(10)] for j in xrange(22)]

        for y in range(py, py+len(mino)) :
            for x in range(px, px+len(mino[0])) :
                b[y][x] = mino[y-py][x-px]

        for y in xrange(len(board)) :
            for x in xrange(len(board[0])):
                #if y-py > 0 and y-py < len(mino) and x-px > 0 and x-px < len(mino[0]) :
                if b[y][x] or board[y][x] : b[y][x] = 1
        return b

    def evaluate(self, board, mino, px):
        ev_ypos = self.fall(board, mino, px)
        ev_space = self.eval_space2(board, mino, px, ev_ypos)
        ev_space_2 = self.eval_space4(board, mino, px, ev_ypos)
        return (ev_ypos+len(mino)-1, ev_space, ev_space_2)

    # refactor
    def think(self, board, current_mino):
        canditate = []
        canditate_tmp = []
        mino = TETRIMINOS[current_mino]

        max_ev_val = 0
        max_xpos = 0
        max_sel = 0
        norm_ev_val = 0
        ypos = 0

        for sel in range(0, len(mino)):
            for xpos in range(0, self.boardsize_x-len(mino[sel][0])+1):
                ev_val = self.evaluate(board, mino[sel], xpos)
                norm_ev_val = float(ev_val[0]) + float(ev_val[1])/1000 + float(ev_val[2])/10000
                if max_ev_val < norm_ev_val :
                    max_ev_val = norm_ev_val
                    max_sel = sel
                    max_xpos = xpos
                    ypos = ev_val[0]

                canditate_tmp.append(norm_ev_val)
            canditate.append(canditate_tmp)
            canditate_tmp = []
        print canditate
        return (max_xpos, max_sel, ypos)

if __name__ == '__main__':

    t = ThinkBombliss(boardsize=(10,22))

    board = [
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [1,1,1,1,1,1,1,1,1,1]]
    print t.think(board,"I")
