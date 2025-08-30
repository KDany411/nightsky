import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars, gui
import PySide6.QtWidgets 
from PySide6.QtGui import QVector3D

app = PySide6.QtWidgets.QApplication(sys.argv)

widget = gui.NoMouseZoom()
widget.setWindowTitle('Night Sky')


widget.addItem(render.stars(stars.observe_stars()))
for line in render.az_polar_axes(): widget.addItem(line)
for line in render.alt_polar_axes(): widget.addItem(line)
widget.addItem(render.create_plane())
widget.addItem(render.create_sphere())
widget.opts['distance'] = 300
widget.opts['center'] = QVector3D(0, 0, 300)
widget.show()

sys.exit(app.exec())
