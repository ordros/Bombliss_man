import capture_bombriss
import think_bombriss
import threading
import time
import cv2

# move to capture_bombriss.py
def whitning(board):
    b = board
    for i in xrange(len(board)):
        if i < 2 :
            b[i] = [0 for x in xrange(len(board[0]))]
    return b

if __name__ == '__main__':
    c = capture_bombriss.CaptureBombriss()
    #t = think_bombriss.ThinkBombriss(boardsize = (capture_bombriss.WINDOW_POS[3]/capture_bombriss.CHIP_X, capture_bombriss.WINDOW_POS[2]/capture_bombriss.CHIP_Y))
    t = think_bombriss.ThinkBombriss(boardsize=(10,22))

    c.parse_next()
    c.parse_chips(cv2.imread("screenshot.png"))
    c.gen_board_img()
    w = c.get_current_mino()
    print t.think(whitning(c.board), "L"),":",w

    while True:
        c.parse_next()
        c.parse_chips()
        w = c.get_current_mino()
        print w + "mino"
        if c.next_flag == 1 :
            c.next_flag = 0
            #c.gen_board_img()
            print "Next!"
            #c.parse_chips(cv2.imread("screenshot.png"))
            print t.think(whitning(c.board), w),":",w
        c.current_mino = c.next_mino
        time.sleep(0.05)
