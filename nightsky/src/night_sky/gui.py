import sys, render
import numpy as np
import PySide6.QtWidgets as qt

def show_camera_altitude(elev, dist=300, radius=1000):
    """Just makes text for the altitude label, adjusts the altitude based on the distance from the center of the sphere"""
    return f"{round(np.rad2deg(np.deg2rad(-elev) + np.arcsin((dist/radius) * np.cos(np.deg2rad(-elev)))), 1)}° "

def show_camera_azimuth(az):
    """Shows which direction the camera is facing in degrees and cardinal directions"""
    real_az = round((-az + 180) %360, 1)
    directions = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N')
    idx = int((real_az + 22.5) // 45)
    return f"{real_az}° {directions[idx]}"

def button_toggle(item, button):
    """Toggles visibility of a single item based on the button state"""
    if button.isChecked():
        item.setVisible(True)
    else:
        item.setVisible(False)
        
def button_toggle_for_lists(item_list, button):
    """Toggles visibility of a list of items based on the button state, used for coordinate lines"""
    if button.isChecked():
        for item in item_list:
            item.setVisible(True)
    else:
        for item in item_list:
            item.setVisible(False)

    

    
    
