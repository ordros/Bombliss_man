
import sys
from itertools import chain
import time

## separate to some file
TETRIMINOS = {
"I":[
    [[1, 1, 1, 1]],

    [[1],
     [1],
     [1],
     [1]]
     ]
     ,
"Z":[
    [[1, 1, 0],
     [0, 1, 1 ]],

    [[0, 1],
     [1, 1],
     [1, 0]]
     ]
     ,
"J":[
    [[1, 1, 1],
     [0, 0, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[1, 1],
     [1, 0],
     [1, 0]]

     ]
     ,
"T":[
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1],
     [1, 1],
     [0, 1]],

    [[0, 1, 0],
     [1, 1, 1]],

    [[1, 0],
     [1, 1],
     [1, 0]]

     ]
     ,
"O":[
    [[1, 1],
     [1, 1]]
     ]
     ,
"S":[
    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 0],
     [1, 1],
     [0, 1]]
     ]
     ,
"L":[
    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1],
     [0, 1],
     [0, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 0],
     [1, 0],
     [1, 1]]
     ]
     ,
 "LJ":[
     [[1, 1, 1],
      [1, 0, 0],
      [1, 0, 0]],

     [[1, 1, 1],
      [0, 0, 1],
      [0, 0, 1]],

     [[0, 0, 1],
      [0, 0, 1],
      [1, 1, 1]],

     [[1, 0, 0],
      [1, 0, 0],
      [1, 1, 1]]
      ]
      ,
  "O1":[
     [[1, 1, 1],
      [0, 1, 1]],

     [[0, 1],
      [1, 1],
      [1, 1]],

     [[1, 1, 0],
      [1, 1, 1]]
      ,
     [[1, 1],
      [1, 1],
      [1, 0]],
      ],
  "O2":[
     [[1, 1, 1],
      [1, 1, 0]],

     [[1, 1],
      [1, 1],
      [0, 1]],

     [[0, 1, 1],
      [1, 1, 1]],

     [[1, 0],
      [1, 1],
      [1, 1]],
      ]
      ,
  "I1":[
     [[1, 1, 1]],

     [[1],
      [1],
      [1]]
      ]
      ,
  "I2":[
     [[1, 1, 1, 1, 1]],

     [[1],
      [1],
      [1],
      [1],
      [1]]
      ]
      ,

  "J1":[
     [[1, 1, 1, 1],
      [0, 0, 0, 1]],

     [[0, 1],
      [0, 1],
      [0, 1],
      [1, 1]],

     [[1, 0, 0, 0],
      [1, 1, 1, 1]],

     [[1, 1],
      [1, 0],
      [1, 0],
      [1, 0]],
      ]
      ,

  "L1":[
     [[1, 1, 1, 1],
      [1, 0, 0, 0]],

     [[1, 1],
      [0, 1],
      [0, 1],
      [0, 1]],

     [[0, 0, 0, 1],
      [1, 1, 1, 1]],

     [[1, 0],
      [1, 0],
      [1, 0],
      [1, 1]],
      ]
}




ILLEGAL_BLOCK = [
    [[1, 1],
     [1, 0],
     [1, 1]],

    [[1, 1],
     [0, 1],
     [1, 1]],

    [[1, 1, 1],
     [1, 0, 1]],

    [[1, 0, 1],
     [1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]],

    [[0, 1],
     [1, 0],
     [1, 0],
     [1, 1]]
]

class ThinkBombliss:
    ##
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
                    if board[ypos+y][xpos+x] == 1 and mino[y][x] == 1 :
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

    def eval_space3(self, board, mino, px, py):
        b = self.compose_mino(board, mino, px, py)
        board_w = self.make_frame(b)
        cnt = 0
        #size = (len(mino)) * (len(mino[0])+2)
        #size = (len(mino)+2) * (len(mino[0])+2)
        #for y in xrange(py-1, py+len(mino)+1):
        size = (len(mino)) * (len(mino[0]))
        for y in xrange(py, py+len(mino)):
            for x in xrange(px, px+len(mino[0])):
                if board[y][x] == 0 : cnt += 1

        #return (size - cnt) / size
        return (size - cnt)

    # refactoring
    def eval_space2(self, board, mino, px, py):
        cnt = 0
        penalty_adjacent = 0
        b = self.compose_mino(board, mino, px, py)
        board_w = make_frame(b)
        for y in xrange(1, len(board)+1):
            for x in xrange(1, len(board[0])+1):
                above = board_w[y+1][x]
                under = board_w[y-1][x]
                left = board_w[y][x-1]
                right = board_w[y][x+1]
                if board_w[y][x] == 0 :
                    if above * under * left * right == 1 :
                        cnt += 1
                        board_w[y][x] = 2
                    if above * under * left == 1 :
                        cnt += 1
                        board_w[y][x] = 2
                    if above * under * right == 1 :
                        cnt += 1
                        board_w[y][x] = 2
                    if above * right * left == 1 :
                        cnt += 1
                        board_w[y][x] = 2
                    if right * under * left == 1 :
                        cnt += 1
                        board_w[y][x] = 2

        for y in xrange(1, len(board)+1):
            for x in xrange(1, len(board[0])+1):
                if board_w[y][x] == 2 :
                    if board_w[y+1][x] == 2 or board_w[y-1][x] == 2 or board_w[y][x+1] == 2 or board_w[y][x-1] == 2 : penalty_adjacent += 1
        #for w in board_w:
        #    print w
        return penalty_adjacent + cnt

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
        #c = [[0 for i in xrange(10)] for j in xrange(22)]
        #print py,len(mino)

        for y in range(py, py+len(mino)) :
            for x in range(px, px+len(mino[0])) :
                #print x,y,px,py
                b[y][x] = mino[y-py][x-px]
        for y in xrange(len(board)) :
            for x in xrange(len(board[0])):
                if b[y][x] == 1 or board[y][x] == 1 : b[y][x] = 1
        return b

    def evaluate(self, board, mino, px):
        ev_ypos = self.fall(board, mino, px)
        ev_space = self.eval_space3(board, mino, px, ev_ypos)
        return (ev_ypos+len(mino)-1, ev_space)

    # refactor
    def think(self, board, current_mino):
        canditate = []
        canditate_tmp = []
        mino = TETRIMINOS[current_mino]
        max_ev_height = 0
        min_ev_space = 1000
        weight_penalty = 5

        for sel in range(0, len(mino)):
            for xpos in range(0,self.boardsize_x-len(mino[sel][0])+1):
                ev_val = self.evaluate(board, mino[sel], xpos)
                norm_ev_val = float(ev_val[0])+float(ev_val[1])/1000
                #norm_ev_val = (float(ev_val[0]), float(ev_val[1]))
                #norm_ev_val = float(ev_val[0])
                canditate_tmp.append(norm_ev_val)
            canditate.append(canditate_tmp)
            canditate_tmp = []

        print canditate
        for i in range(0, len(canditate)) :
            for j in range(0, len(canditate[i])):
                if max_ev_height < canditate[i][j]:
                    max_ev_height = canditate[i][j]
                    max_xpos = j
                    max_sel = i
        return (max_xpos, max_sel, self.fall(board, mino[max_sel], max_xpos))
#       return (max_xpos, max_sel)

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
         [1,1,0,0,0,1,1,1,1,1]]
    print t.think(board,"L")
