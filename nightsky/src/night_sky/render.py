import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt6.QtWidgets import QApplication
import sys

def spherical_to_cartesian(theta, phi, radius=1):
    """Convert spherical coordinates to Cartesian coordinates."""
    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
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
        app.setCameraPosition(distance=0.2, elevation=0, azimuth=0)
    app.show()

def stars(star_data):
    list_of_stars = []
    for star in star_data:
        theta, phi = star.alt, star.az
        x, y, z = spherical_to_cartesian(phi, theta)
        sphere = gl.GLScatterPlotItem(pos=[(x, y, z)], size= (-star.magnitude + 8)/2, color=(0.5, 0.5, 1, 0.5))
        sphere.setGLOptions('opaque')
        list_of_stars.append(sphere)
    return list_of_stars
