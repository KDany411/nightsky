import pyqtgraph as pg
import pyqtgraph.opengl as gl
import PySide6.QtWidgets as QtWidgets
import sys

NightSkyApp = QtWidgets.QApplication(sys.argv)

from render import create_sphere
create_sphere()