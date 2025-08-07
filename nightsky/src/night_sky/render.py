import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PySide6.QtCore import QTimer
import sys

def spherical_to_cartesian(alt, az, radius=999):
    """Convert spherical coordinates to Cartesian coordinates."""
    theta = np.pi / 2 - alt
    x = radius * np.sin(theta) * np.cos(az)
    y = radius * np.sin(theta) * np.sin(az)
    z = radius * np.cos(theta)
    return x, y, z

def create_sphere(radius=1, rows=20, cols=20):
    """Create a sphere mesh and show it"""
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows=50, cols=50, radius=1),
        smooth=True)
    mesh.setColor((0, 0, 0, 0))
    mesh.setGLOptions('translucent')
    return mesh

def create_plane():
    """Create a plane mesh."""
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData(vertexes=np.array([
            [0, -1, 1],
            [0, -1, -1],
            [0, 1, -1],
            [0, 1, 1]
        ]), faces=np.array([
            [0, 1, 2],
            [0, 2, 3]
        ])))
    return mesh

def view(renderable_objects):
    """Main function to run the application."""
    app = gl.GLViewWidget()
    app.setWindowTitle('Night Sky')
    for object in renderable_objects:
        if type(object) == list:
            for item in object:
                app.addItem(item)
        else: 
            app.addItem(object)
        app.setCameraPosition(distance=5, elevation=0, azimuth=0)
    app.show()
    print(start_camera_logger(app))

def stars(star_data):
    cords, magnitude = [], []
    for star in star_data:
        cords.append(spherical_to_cartesian(star.alt, star.az))
        magnitude.append((-star.magnitude + 7) * 1.2)
    sphere = gl.GLScatterPlotItem(pos=cords, size=magnitude, color=(1, 1, 1, 1), pxMode=False)
    sphere.setGLOptions('opaque')
    return sphere

def alt_polar_axes(r=1000):
    axis_alt = [gl.GLLinePlotItem(pos=np.array([[r*np.cos(np.deg2rad(angle))*float(np.cos(np.pi/72 * a)), r*np.cos(np.deg2rad(angle))*float(np.sin(np.pi/72 * a)), r*np.sin(np.deg2rad(angle))] for a in np.arange(145)]), color=(0.5, 0.5, 0.5, 0.5), width=2) for angle in np.arange(-180,180,10)]
    return axis_alt

def az_polar_axes(r=1000):
    axis_az = [gl.GLLinePlotItem(pos=np.array([[r*np.sin(np.deg2rad(angle))*np.sin(np.pi/72*a), r*np.cos(np.deg2rad(angle))*np.sin(np.pi/72*a), r*np.cos(np.pi/72*a)] for a in np.arange(145)]), color=(0.5, 0.5, 0.5, 0.5), width=2) for angle in np.arange(0, 180, 10)]
    return axis_az
