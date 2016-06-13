import capture_bombliss
import think_bombliss
import threading
import time
import cv2
import socket
from config_bombliss import ALIGN

class BomblissMan:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def go(self):
        c = capture_bombliss.CaptureBombliss()
        t = think_bombliss.ThinkBombliss(boardsize=(10,22))
        #c.parse_next()

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.server, self.port))

        while True:
            c.parse_next()
            c.parse_chips()
            w = c.get_current_mino()
            print w + "mino"
            if c.check_next() :
                #c.gen_board_img()
                print "Next!"
                choice = t.think(c.whitning_board(c.board), w)
                #print choice,":", w
                al = ALIGN[w][int(choice[1])]
                # xpos, sel, ypos, align
                msg = str(choice[0] - al)+"_"+str(choice[1])+"_"+str(choice[2])
                msg = msg + " "*(30 - len(msg))
                print w+"mino, xpos: "+str(choice[0])+", sel: "+str(choice[1])+", ypos: "+str(choice[2])
                soc.send(msg)
                #c.current_mino = c.next_mino
            time.sleep(0.02)

if __name__ == '__main__':

    server = "192.168.10.148"
    port = 50000

    b = BomblissMan(server, port)
    b.go()
