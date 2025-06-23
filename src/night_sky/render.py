import pyqtgraph as pg
import pyqtgraph.opengl as gl
import PySide6.QtWidgets as QtWidgets
import sys

def spherical_to_cartesian(radius, theta, phi):
    """Convert spherical coordinates to Cartesian coordinates."""
    x = radius * pg.math.sin(theta) * pg.math.cos(phi)
    y = radius * pg.math.sin(theta) * pg.math.sin(phi)
    z = radius * pg.math.cos(theta)
    return x, y, z

def create_sphere(radius=1, rows=20, cols=20):
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows=20, cols=20, radius=1),
        smooth=True, color=(1, 1, 1, 0.5))
    sphere = gl.GLViewWidget()
    sphere.addItem(mesh)
    sphere.setCameraPosition(distance=0.01, elevation=0, azimuth=0)
    sphere.show()
    pg.exec()