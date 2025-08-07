import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars
import PySide6.QtWidgets 

app = PySide6.QtWidgets.QApplication(sys.argv)

widget = gl.GLViewWidget()
widget.setWindowTitle('Night Sky')

widget.addItem(render.stars(stars.observe_stars()))
for line in render.alt_polar_axes(): widget.addItem(line)
for line in render.az_polar_axes(): widget.addItem(line)
widget.addItem(render.create_sphere())
widget.setCameraPosition(distance=5, elevation=0, azimuth=0)
widget.show()

sys.exit(app.exec())
