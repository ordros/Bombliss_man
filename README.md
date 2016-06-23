BomblissMan
====

## Description
Bombliss AI on SNES.    
Using OpenCV, Python2.7, and Raspberry Pi(to operate SNES)  

## Requirement(Library)
cv2, pyautogui, PyYaml
Please install from pip  
## Requirement(Device)
USB capture device and Raspberry Pi.  
I use GV-USB2(IODATA) and Raspberry Pi 2B.  

## Usage
Edit window in config_bombliss_snes.yaml to adjust your environment.  
position(left-up-corner), size = [x, y]   

Modify SNES controller so that Raspberry Pi can operate this with GPIO access.   

On Raspberry Pi,  
`$python control_bombliss.py`  
and advance Bombliss until game start.  
On computer of capturing SNES,  
`$python main.py`
then start AI.
