import capture_bombliss
import think_bombliss
import threading
import time
import cv2
import socket

ALIGN = {
        "I":[3, 5],
        "Z":[3, 3],
        "J":[3, 3, 3, 4],
        "T":[3, 3, 3, 4],
        "O":[4],
        "S":[3, 3],
        "L":[3, 3, 3, 4],
        "LJ":[4, 3, 3, 4],
        "I2":[2, 4],
        "I1":[3, 4],
        "L1":[3, 4, 3, 4],
        "J1":[3, 4, 3, 4],
        "O1":[3, 3, 3, 4],
        "O2":[3, 3, 3, 4]
        }

class BomblissMan:
    def __init__(self, server, port):
        self.server = server
        self.port = port

    def go(self):
        c = capture_bombliss.CaptureBombliss()
        t = think_bombliss.ThinkBombliss(boardsize=(10,22))
        c.parse_next()

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((self.server, self.port))

        while True:
            c.parse_next()
            c.parse_chips()
            w = c.get_current_mino()
            print w + "mino"
            if c.next_flag == 1 :
                c.next_flag = 0
                #c.gen_board_img()
                print "Next!"
                choice = t.think(c.whitning_board(c.board), w)
                print choice,":",w
                al = ALIGN[w][int(choice[1])]
                # xpos, sel, ypos, align
                soc.send(str(choice[0])+"_"+str(choice[1])+"_"+str(choice[2])+"_"+str(al))

            c.current_mino = c.next_mino
            time.sleep(0.01)

if __name__ == '__main__':

    server = "192.168.10.148"
    port = 50000

    b = BomblissMan(server, port)
    b.go()
