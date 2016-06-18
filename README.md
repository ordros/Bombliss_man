BomblissMan
====

## Description
Bombliss AI on SFC.    
Using OpenCV, Python2.7, and Raspberry Pi(to operate SFC)  
## Usage
Edit WINDOW_POS, NEXT_POS in config_bombliss.py to adjust your environment.  
WINDOW_POS = (a, b, c, d)  
a, b is position top left corner of board.  
c, d is boardsize of x-axis and y-axis.  

Modify SFC Controller so that Raspberry Pi can operate this with GPIO access.   

On Raspberry Pi,  
`$python control_bombliss.py`  
On computer of capturing SFC,  
`$python main.py`
