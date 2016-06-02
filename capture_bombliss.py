import pyautogui as p
import cv2
import time
import numpy as np
import os

## separate to config files?
NEXT_MINOS = {0:"I", 1:"Z", 2:"J", 3:"O", 4:"S", 5:"T", 6:"L", 7:"LJ"}

WINDOW_POS = (1308, 273, 270, 528) # xpos, ypos, window_xsize, window_ysize
NEXT_POS = (1391, 233, 100, 30)
NEXT_IMGS = ["next_imgs/"+x[1]+"_binary.png" for x in NEXT_MINOS.items()]

CHIP_X = 27
CHIP_Y = 24

class CaptureBombliss:
    def __init__(self):
        self.next_mino = 0
        self.current_mino = 0
        self.next_flag = 0
        self.cnt = 0

        self.board = [[None for c in range(WINDOW_POS[2]/CHIP_X)] for l in range(WINDOW_POS[3]/CHIP_Y)]

        self.boardsize_x = (WINDOW_POS[2]/CHIP_X)
        self.boardsize_y = (WINDOW_POS[3]/CHIP_Y)

    @property
    def board(self):
        return self.board

    @board.setter
    def board(self, value):
        self.board = value

    def whitning_board(self, board):
        b = board
        for i in xrange(len(board)):
            if i < 2 :
                b[i] = [0 for x in xrange(len(board[0]))]
        return b

    def get_current_mino(self):
        return NEXT_MINOS[self.current_mino]

    def capture_window(self, (x, y, window_x, window_y)):
        screen = p.screenshot(region = (x, y, window_x, window_y))
        img = np.asarray(screen)
        return img

## refactoring flag process
    def parse_chips(self, clp = None):
        num_stop = 3
        board = self.board
        if clp == None : clp = self.capture_window(WINDOW_POS)
        for y in range(CHIP_Y, len(clp)+1, CHIP_Y):
            for x in range(CHIP_X, len(clp[0])+1, CHIP_X):
                #cv2.imwrite("chips/"+str(y)+"_"+str(x)+".png", clp[y-CHIP_Y:y-1, x-CHIP_X:x-1])
                chip = clp[y-CHIP_Y:y-1, x-CHIP_X:x-1]
                if self.decide_chip2(chip):
                    board[y/CHIP_Y-1][x/CHIP_X-1] = 0
                else:
                    board[y/CHIP_Y-1][x/CHIP_X-1] = 1
        self.board = board
        self.cnt += 1

        if self.next_flag == 0 and (sum(board[0]) > 0 or sum(board[1])) and self.cnt > num_stop:
            self.next_flag = 1
            self.cnt = 0
            return

        if self.next_flag == 1 :
            self.next_flag = 0
            return

## refactoring flag process
    def parse_next(self, clp = None):
        if clp == None : img = self.capture_window(NEXT_POS)
        img = cv2.GaussianBlur(img, (11,11), 0)
        img = self.binarize(img)
        #cv2.imwrite("lj_binary.png", img)
        cor = []
        for i in NEXT_IMGS:
            img_t = cv2.imread(i)
            cor.append(self.diff(img, img_t))

        if not self.current_mino == self.next_mino:
            self.next_flag = 1
            self.current_mino = self.next_mino

        self.next_mino = cor.index(max(cor))

## deprecated?
    def calc_chips_avg(self, chip1, chip2, chip3, chip4):
        chip_avg = []
        for i in range(0,3):
            chip_avg.append((int(chip1[i]) + int(chip2[i]) + int(chip3[i]) + int(chip4[i]))/4)
        return chip_avg

    def decide_chip(self, chip):
        p = chip[len(chip)/2][len(chip[0])/2]
        if p[0] < 100 and p[1] < 100 and p[2] < 100 : return True
        else: return False

    def gen_board_img(self, name = "board.png"):
        board = self.board
        posy_img = WINDOW_POS[3]/CHIP_Y # 22
        posx_img = WINDOW_POS[2]/CHIP_X # 10
        img = np.zeros((posy_img, posx_img, 3), np.uint8)

        for i in range(0, posy_img):
            for j in range(0, posx_img):
                if board[i][j] == 1 : img[i, j] = [255, 255, 255]
                else : img[i, j] = [0, 0, 0]

        img = cv2.resize(img, (posx_img*10, posy_img*10), interpolation=cv2.cv.CV_INTER_NN)
        cv2.imwrite(name, img)

## replace with cv2.threshold
    def binarize(self, img):
        out = [[0 for x in xrange(len(img[0]))] for y in xrange(len(img))]

        for y in xrange(len(img)):
            for x in xrange(len(img[0])):
                p = img[y][x]
                if p[0] > 100 or p[1] > 100 or p[2] > 100:
                    out[y][x] = [0, 0, 0]
                else :
                    out[y][x] = [255, 255, 255]
        return np.array(out)

    def diff(self, img1, img2):
        cnt = 0
        p = 0
        out = [[0 for x in xrange(len(img1[0]))] for y in xrange(len(img1))]
        for y in xrange(len(img1)):
            for x in xrange(len(img1[0])):
                if list(img1[y][x]) == list(img2[y][x]) :
                    cnt += 1
                    out[y][x] = [255, 255, 255]
                else : out[y][x] = [0, 0, 0]
            #if cnt >  : p += 1
            #cnt = 0
        return cnt


if __name__ == '__main__':

    b = CaptureBombliss()
    b.parse_next()
    #b.parse_chips()

"""
    while True:
        b.parse_next()
        b.parse_chips()

        print "Next: "+NEXT_MINOS[b.next_mino]+"mino", b.next_flag
        if b.next_flag == 1: print "Next!"
        b.gen_board_img()
        time.sleep(0.5)
"""
