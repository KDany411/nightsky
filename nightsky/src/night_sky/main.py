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
label = qt.QLabel()
crosshair = qt.QLabel("+")

#APP WINDOW
main_window = qt.QMainWindow()
main_window.resize(1000, 750)

#FIRST LAYER
central_widget = qt.QWidget()
main_window.setCentralWidget(central_widget)
central_widget_layout = qt.QStackedLayout()
central_widget_layout.setStackingMode(qt.QStackedLayout.StackAll)
central_widget.setLayout(central_widget_layout)
central_widget_layout.addWidget(view_widget)
#SECOND LAYER
GUI_widget = qt.QWidget()
central_widget_layout.addWidget(GUI_widget)
GUI_widget.raise_()
GUI_layout = qt.QVBoxLayout()
GUI_widget.setLayout(GUI_layout)
label.setFont(QFont('Microsoft Sans Serif', 12))
GUI_widget.setAttribute(qc.Qt.WA_TransparentForMouseEvents, True)
GUI_layout.addWidget(label, 0, Qt.AlignmentFlag.AlignTop)
GUI_layout.addWidget(crosshair, 0, Qt.AlignmentFlag.AlignCenter)
placeholder_widget = qt.QWidget()
GUI_layout.addWidget(placeholder_widget, 0, Qt.AlignmentFlag.AlignBottom)

main_window.setWindowTitle('Night Sky')



view_widget.setGeometry(0, 0, 1000, 750)
label.setGeometry(10, 10, 150, 50)
label.setStyleSheet("color:white")
crosshair.setStyleSheet("color:red")


def wrapper_for_az_and_ele_gui():
    az = gui.show_camera_azimuth(view_widget.opts['azimuth'])
    elev = gui.show_camera_elevation(view_widget.opts['elevation'])
    label.setText(f" az:  {az}\n alt: {elev}")



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
