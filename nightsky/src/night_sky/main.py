import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars
import PySide6.QtWidgets 

qapp = PySide6.QtWidgets.QApplication(sys.argv)
a = render.create_sphere()
b = render.stars(stars.observe_stars())
c = render.coordinate_polar_axes()
#c = render.create_plane()
render.view((b,a,c))
sys.exit(qapp.exec())
