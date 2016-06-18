BomblissMan
====

## Description
Bombliss AI on SNES.    
Using OpenCV, Python2.7, and Raspberry Pi(to operate SNES)  

## Requirement(Library)
cv2, pyautogui  
## Requirement(Device)
USB capture device and Raspberry Pi.  
I use GV-USB2(IODATA) and Raspberry Pi 2B.  

## Usage
Edit WINDOW_POS, NEXT_POS in config_bombliss.py to adjust your environment.  
WINDOW_POS = (a, b, c, d)  
a, b is position top left corner of board.  
c, d is boardsize of x-axis and y-axis.  

Modify SNES Controller so that Raspberry Pi can operate this with GPIO access.   

On Raspberry Pi,  
`$python control_bombliss.py`  
On computer of capturing SNES,  
`$python main.py`
