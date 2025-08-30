import sys
import PySide6.QtWidgets as qt
import pyqtgraph.opengl as gl

class NoMouseZoom(gl.GLViewWidget):
    def wheelEvent(self, ev):
       pass

