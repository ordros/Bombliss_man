import pyautogui as p
import cv2
import time
import numpy as np
import os

from config_bombliss import NEXT_MINOS, WINDOW_POS, NEXT_POS, NEXT_IMGS, CHIP_X, CHIP_Y

class CaptureBombliss:
    def __init__(self):
        self.next_mino = 0
        self.current_mino = 0
        self.cnt = 0

        self.board = [[None for c in range(WINDOW_POS[2]/CHIP_X)] for l in range(WINDOW_POS[3]/CHIP_Y)]

        self.boardsize_x = (WINDOW_POS[2]/CHIP_X)
        self.boardsize_y = (WINDOW_POS[3]/CHIP_Y)
        self.imgs_next = [cv2.imread(x) for x in NEXT_IMGS]

    @property
    def board(self):
        return self.board

    @board.setter
    def board(self, value):
        self.board = value

    def whitning_board(self, board):
        #b = board
        for i in xrange(len(board)):
            if i < 2 :
                board[i] = [0 for x in xrange(len(board[0]))]
        return board

    def get_current_mino(self):
        return NEXT_MINOS[self.current_mino]

    def capture_window(self, (x, y, window_x, window_y)):
        screen = p.screenshot(region = (x, y, window_x, window_y))
        img = np.asarray(screen)
        return img


    def check_next(self):
        board = self.board
        num_stop = 5
        self.cnt += 1
        if (not self.current_mino == self.next_mino) and self.cnt > num_stop:
            print "change.", self.cnt
            self.current_mino = self.next_mino
            self.cnt = 0
            return True

        if (sum(board[0]) > 0 or sum(board[1]) > 0) and self.cnt > num_stop:
            print "glimpse.", self.cnt
            self.cnt = 0
            return True
        return False

## refactoring flag process
    def parse_chips(self, clp = None):
        board = self.board
        if clp == None : clp = self.capture_window(WINDOW_POS)
        for y in range(CHIP_Y, len(clp)+1, CHIP_Y):
            for x in range(CHIP_X, len(clp[0])+1, CHIP_X):
                #cv2.imwrite("chips/"+str(y)+"_"+str(x)+".png", clp[y-CHIP_Y:y-1, x-CHIP_X:x-1])
                chip = clp[y-CHIP_Y:y-1, x-CHIP_X:x-1]
                if self.decide_chip(chip):
                    board[y/CHIP_Y-1][x/CHIP_X-1] = 0
                else:
                    board[y/CHIP_Y-1][x/CHIP_X-1] = 1
        self.board = board

## refactoring flag process
    def parse_next(self, clp = None):
        rate_comp = 1
        if clp == None : img = self.capture_window(NEXT_POS)
        img = cv2.GaussianBlur(img, (11,11), 0)
        #img = cv2.resize(img, (len(img[0])/rate_comp, len(img)/rate_comp))
        img = self.binarize(img)
        cor = []
        #img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        #cv2.imwrite("lj_binary.png", img)

        for i in self.imgs_next:
            #i = cv2.resize(i, (len(i[0])/rate_comp, len(i)/rate_comp), interpolation=cv2.cv.CV_INTER_NN)
            cor.append(self.diff(img, i))

        self.next_mino = cor.index(max(cor))

    def decide_chip(self, chip):
        p = chip[len(chip)/2][len(chip[0])/2]
        if p[0] < 100 and p[1] < 100 and p[2] < 100 : return True
        return False

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
        for y in xrange(len(img1)):
            for x in xrange(len(img1[0])):
                if list(img1[y][x]) == list(img2[y][x]) :
                    cnt += 1
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
