import capture_bombliss
import think_bombliss
import time
import cv2
from config_bombliss import ALIGN
import gen_config
g = gen_config.generateConfig(config_file="config/config_bombrite.yaml")
g.gen_configfile()

import pyautogui as p
from control_key import move_up, move_down, move_left, move_right, move_turn, press_start, press
import multiprocessing

def move(xp,sel,yp,al):
    xp = xp - al
    move_turn(sel)
    if xp < 0:
        move_left(abs(xp))
    else:
        move_right(xp)
    move_down(yp/5)

class BombriteMan:
    def __init__(self):
        pass
    def go(self):
        c = capture_bombliss.CaptureBombliss()
        t = think_bombliss.ThinkBombliss(boardsize=(10,22))

        c.parse_board()
        c.current_mino = -1
        print "WAIT..."
        time.sleep(1)
        print "GO."
        press_start()


        while True:
            c.parse_board()
            w = c.get_current_mino()
            print w + "mino"
            if c.check_next() :
                print "============"
                print "Next!", c.cnt
                choice = t.think(c.whitning_board(c.board), w)
                al = ALIGN[w][int(choice[1])]
                # xpos, sel, ypos, align
                job = multiprocessing.Process(target=move, args=(choice[0], choice[1], choice[2], al))
                job.start()
                print w+"mino, xpos: "+str(choice[0])+", sel: "+str(choice[1])+", ypos: "+str(choice[2])
                print "============"
                c.current_mino = c.next_mino
                #c.gen_board_img()
            time.sleep(0.001)

if __name__ == '__main__':
    b = BombriteMan()
    b.go()
