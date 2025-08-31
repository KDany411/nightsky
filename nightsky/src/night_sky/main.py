import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars, gui
import PySide6.QtWidgets 
from PySide6.QtGui import QVector3D

app = PySide6.QtWidgets.QApplication(sys.argv)
main_window = PySide6.QtWidgets.QMainWindow()
central_widget = PySide6.QtWidgets.QWidget()
main_window.setCentralWidget(central_widget)
layout = PySide6.QtWidgets.QVBoxLayout()
central_widget.setLayout(layout)
main_window.setWindowTitle('Night Sky')
view_widget = render.NoMouseZoom()
print(type(view_widget))
layout.addWidget(view_widget)

view_widget.addItem(render.stars(stars.observe_stars()))
for line in render.az_polar_axes(): view_widget.addItem(line)
for line in render.alt_polar_axes(): view_widget.addItem(line)
view_widget.addItem(render.create_plane())
view_widget.addItem(render.create_sphere())
view_widget.opts['distance'] = 300
view_widget.opts['center'] = QVector3D(0, 0, 300)

view_widget.show()

sys.exit(app.exec())
