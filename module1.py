import numpy as np
import tkinter as tk
from subtractor import subtractor

sub = subtractor('Static_cam_vid.mp4', 'mog2', showfps=True, masksource=False, saveVid=True)
print(sub.type)

sub.showMask()  
