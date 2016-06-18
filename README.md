BomblissMan
====

## Description
Bombliss AI on SNES.    
Using OpenCV, Python2.7, and Raspberry Pi(to operate SNES)  

## Requirement
#Python
cv2, pyautogui
#Device
USB capture device.
I use GV-USB2(IODATA)


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
