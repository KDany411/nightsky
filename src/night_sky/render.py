import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QApplication
import sys

def spherical_to_cartesian(theta, phi, radius=1):
    """Convert spherical coordinates to Cartesian coordinates."""
    x = radius * pg.math.sin(theta) * pg.math.cos(phi)
    y = radius * pg.math.sin(theta) * pg.math.sin(phi)
    z = radius * pg.math.cos(theta)
    return x, y, z

def create_sphere(radius=1, rows=20, cols=20):
    """Create a sphere mesh and show it"""
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows=50, cols=50, radius=1),
        smooth=True, shader='shaded')
    sphere = gl.GLViewWidget()
    sphere.addItem(mesh)
    sphere.setCameraPosition(distance=10, elevation=10, azimuth=10)
    sphere.show()
    
def app(function: callable):
    """Main function to run the application."""
    app = QApplication(sys.argv)
    function()
    sys.exit(app.exec())

