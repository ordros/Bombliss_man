import unittest
import sys, os
sys.path.append(os.getcwd())
import think_bombliss
from capture_bombliss import WINDOW_POS, CHIP_X, CHIP_Y

class CaptureTest(unittest.TestCase):
    def test_fall(self):
        sizex = WINDOW_POS[2]/CHIP_X
        sizey = WINDOW_POS[3]/CHIP_Y

        c = think_bombliss.ThinkBombliss((sizex, sizey))
        board =  [[0 for i in range(WINDOW_POS[2]/CHIP_X)] for j in range(WINDOW_POS[3]/CHIP_Y)]
        minos = think_bombliss.TETRIMINOS

        for mino in minos.values():
            for sel in xrange(len(mino)):
                for x in xrange(sizex):
                    #print len(mino[sel][0]), x, len(board[0])
                    self.assertRaises(Exception, c.fall, (board, mino[sel], x))

unittest.main()
