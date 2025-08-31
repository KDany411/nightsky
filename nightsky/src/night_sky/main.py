import os

os.environ["PYQTGRAPH_QT_LIB"] = "PySide6"

import pyqtgraph.opengl as gl
import sys
import render, stars, gui
import PySide6.QtWidgets as qt
import PySide6.QtCore as qc
from PySide6.QtCore import Qt
from PySide6.QtGui import QVector3D

# CHAOS

app = qt.QApplication(sys.argv)
main_window = qt.QMainWindow()
main_window.resize(1000, 750)
central_widget = qt.QWidget()
main_window.setCentralWidget(central_widget)
layout = qt.QStackedLayout()
central_widget.setLayout(layout)
main_window.setWindowTitle('Night Sky')
view_widget = render.NoMouseZoom()
layout.addWidget(view_widget)
label = qt.QLabel()

label.setStyleSheet("color:white")


def wrapper_for_az_and_ele_gui():
    az = gui.show_camera_azimuth(view_widget.opts['azimuth'])
    elev = gui.show_camera_elevation(view_widget.opts['elevation'])
    label.setText(f" az:  {az}\n alt: {elev}")
layout.addWidget(label)
label.raise_()
layout.setAlignment(label, Qt.AlignTop)
layout.setContentsMargins(10, 10, 0, 0) 
label.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)
layout.setStackingMode(qt.QStackedLayout.StackAll)
timer = qc.QTimer()
timer.timeout.connect(wrapper_for_az_and_ele_gui)
timer.start(10)
view_widget.addItem(render.stars(stars.observe_stars()))
for line in render.az_polar_axes(): view_widget.addItem(line)
for line in render.alt_polar_axes(): view_widget.addItem(line)
#view_widget.addItem(render.create_plane())
view_widget.addItem(render.create_sphere())
view_widget.opts['distance'] = 300
view_widget.opts['center'] = QVector3D(0, 0, 300)
view_widget.opts['azimuth'] = 0
view_widget.opts['elevation'] = 0

main_window.show()

sys.exit(app.exec())
