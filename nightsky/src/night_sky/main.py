import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars
from PySide6.QtWidgets import QApplication

qapp = QApplication(sys.argv)
a = (render.create_sphere())
b = render.stars(stars.observe_stars())
render.view((b,a))
sys.exit(qapp.exec())
