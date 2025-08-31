import sys, render
import numpy as np
import PySide6.QtWidgets as qt


def show_camera_elevation(elev, dist=300, radius=1000):
    return f"{round(np.rad2deg(np.deg2rad(-elev) + np.arcsin((dist/radius) * np.cos(np.deg2rad(-elev)))), 1)}° "

def show_camera_azimuth(az):
    real_az = round(az%360, 1)
    directions = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N')
    idx = int((real_az + 22.5) // 45)
    return f"{real_az}° {directions[idx]}"

    

    

    
    
