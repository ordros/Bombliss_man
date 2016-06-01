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
        "I2":[2, 4]
        }



# move to capture_bombriss.py
if __name__ == '__main__':
    c = capture_bombliss.CaptureBombliss()
    #t = think_bombriss.ThinkBombriss(boardsize = (capture_bombriss.WINDOW_POS[3]/capture_bombriss.CHIP_X, capture_bombriss.WINDOW_POS[2]/capture_bombriss.CHIP_Y))
    t = think_bombliss.ThinkBombliss(boardsize=(10,22))

    c.parse_next()
#    c.parse_chips(cv2.imread("screenshot.png"))
#    c.gen_board_img()
#    w = c.get_current_mino()
#    print t.think(whitning(c.board), "L"),":",w

    server = "192.168.10.148"
    port = 50000

    #s = ControlBombliss(0)
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((server, port))

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
            choice = t.think(c.whitning_board(c.board), w)
            print choice,":",w
            al = ALIGN[w][int(choice[1])]
            # xpos, sel, ypos, align
            print al
            soc.send(str(choice[0])+"_"+str(choice[1])+"_"+str(choice[2])+"_"+str(al))

        c.current_mino = c.next_mino
        time.sleep(0.01)
