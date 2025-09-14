import os
os.environ["PYQTGRAPH_QT_LIB"] = "PySide6"
import pyqtgraph.opengl as gl
import sys
import render, stars, gui
import PySide6.QtWidgets as qt
import PySide6.QtCore as qc
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QVector3D

app = qt.QApplication(sys.argv)

#WIDGETS
view_widget = render.NoMouseZoom()
view_widget.setGeometry(0, 0, 1000, 750)
label = qt.QLabel()
crosshair = qt.QLabel("+")

#APP WINDOW
main_window = qt.QMainWindow()
main_window.resize(1000, 750)
main_window.setWindowTitle('Night Sky')

# THE WHOLE WINDOW
# Basically the parent widget containing everything
central_widget = qt.QWidget()
main_window.setCentralWidget(central_widget)
central_widget_layout = qt.QVBoxLayout()
central_widget.setLayout(central_widget_layout)

# MAIN WIDGET
# Widget with the 3D view and the overlay (live coordinate tracking, crosshair)
main_widget = qt.QWidget()
main_widget_layout = qt.QStackedLayout()
main_widget.setLayout(main_widget_layout)
main_widget_layout.setStackingMode(qt.QStackedLayout.StackAll)
main_widget_layout.addWidget(view_widget)
main_widget.raise_()
central_widget_layout.addWidget(main_widget)

# RENDERABLES
# functions from render.py generating objects that are rendered in the 3D view
# in order: horizon plane, stars plot, horizontal coordinate lines, sun, moon, equatorial coordinate lines
# in the second part they are added to the 3D view, for the coordinates lines each line is added separately

plane = render.create_plane()
starz = render.create_stars(stars.observe_stars())
az = render.az_polar_axes()
alt = render.alt_polar_axes()
sun = render.sun(stars.get_sun_position())
moon = render.moon(stars.get_moon_position())
dec = render.dec_polar_axis()
ra = render.ra_polar_axis()

view_widget.addItem(plane)
view_widget.addItem(starz)
for line in az: view_widget.addItem(line)
for line in alt: view_widget.addItem(line)
for line in dec: view_widget.addItem(line)
for line in ra: view_widget.addItem(line)
view_widget.addItem(sun)
view_widget.addItem(moon)


#OVERLAY WIDGET
# widget on top of the 3D view containing the labels of altitude, azimuth and the crosshair
overlay_widget = qt.QWidget()
main_widget_layout.addWidget(overlay_widget)
overlay_widget.raise_()
overlay_layout = qt.QVBoxLayout()
overlay_widget.setLayout(overlay_layout)
overlay_widget.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)

# LABEL OF ALT, AZ
# dynamically updated label showing the azimuth and altitude of the point at which the camera is pointing
label.setFont(QFont('Microsoft Sans Serif', 12))
label.setGeometry(10, 10, 150, 50)
label.setStyleSheet("color:white")

def wrapper_for_az_and_ele_gui():
    az = gui.show_camera_azimuth(view_widget.opts['azimuth'])
    elev = gui.show_camera_altitude(view_widget.opts['elevation'])
    label.setText(f" az:  {az}\n alt: {elev}")

# the timer updates the label every 10 ms
timer = qc.QTimer()
timer.timeout.connect(wrapper_for_az_and_ele_gui)
timer.start(10)
overlay_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignTop)

#CROSSHAIR
overlay_layout.addWidget(crosshair, 0, Qt.AlignmentFlag.AlignCenter)
crosshair.setStyleSheet("color:red")

#CROSSHAIR CENTERING
placeholder_widget = qt.QWidget()
overlay_layout.addWidget(placeholder_widget, 0, Qt.AlignmentFlag.AlignBottom)

# BUTTONS BAR
# using the widget hiarchy to create a bar with buttons
buttons_bar = qt.QWidget()
top_bar_layout = qt.QHBoxLayout()
buttons_bar.setLayout(top_bar_layout)
buttons_bar.setAttribute(qc.Qt.WA_TransparentForMouseEvents, False)
central_widget_layout.addWidget(buttons_bar, 0, Qt.AlignmentFlag.AlignTop)

# BUTTONS
# each button is connected to a function in gui.py that toggles visibility of the corresponding object,
# those are the buttons at the bottom of the window
horizont_button = qt.QPushButton("Horizon")
horizont_button.setCheckable(True)
horizont_button.setChecked(True)
horizont_button.setStyleSheet("QPushButton {background-color: lightgrey; color: black} QPushButton:checked {background-color: darkblue; color: white}")
top_bar_layout.addWidget(horizont_button, 1)
horizont_button.toggled.connect(lambda: gui.button_toggle(plane, horizont_button))

Hcoordinates_button = qt.QPushButton(" Horizontal Coordinates")
Hcoordinates_button.setCheckable(True)
Hcoordinates_button.setChecked(True)
Hcoordinates_button.setStyleSheet("QPushButton {background-color: lightgrey; color: black} QPushButton:checked {background-color: darkblue; color: white}")
top_bar_layout.addWidget(Hcoordinates_button, 1)
Hcoordinates_button.toggled.connect(lambda: gui.button_toggle_for_lists(az + alt, Hcoordinates_button))

Ecoordinates_button = qt.QPushButton("Equatorial Coordinates")
Ecoordinates_button.setCheckable(True)
Ecoordinates_button.setChecked(True)
Ecoordinates_button.setStyleSheet("QPushButton {background-color: lightgrey; color: black} QPushButton:checked {background-color: darkblue; color: white}")
top_bar_layout.addWidget(Ecoordinates_button, 1)
Ecoordinates_button.toggled.connect(lambda: gui.button_toggle_for_lists(ra + dec, Ecoordinates_button))

# CAMERA SETTINGS
# setup so the camera doesn't colide with the horizon plane when rotating,
# this makes the camera float above the plane and distorts the view of the sky a bit
view_widget.opts['distance'] = 300
view_widget.opts['center'] = QVector3D(0, 0, 300)
view_widget.opts['azimuth'] = 0
view_widget.opts['elevation'] = 0

main_window.show()
sys.exit(app.exec())
