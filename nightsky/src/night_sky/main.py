import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars
from PySide6.QtWidgets import QApplication

qapp = QApplication(sys.argv)
a = (render.create_sphere())
b = render.stars(stars.observe_stars())
c = render.create_plane()
render.view((b,c,a))
sys.exit(qapp.exec())
