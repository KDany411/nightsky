import pyqtgraph as pg
import pyqtgraph.opengl as gl
import sys
import render, stars
import PySide6.QtWidgets 

qapp = PySide6.QtWidgets.QApplication(sys.argv)
a = render.create_sphere()
b = render.stars(stars.observe_stars())
c = render.alt_polar_axes()
d = render.az_polar_axes()  
#c = render.create_plane()
render.view((b,c,d,a))
sys.exit(qapp.exec())
