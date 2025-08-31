import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PySide6.QtCore import QTimer
from PySide6 import QtCore
import sys

class NoMouseZoom(gl.GLViewWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def wheelEvent(self, ev):
        pass
    def mouseMoveEvent(self, ev):
        lpos = ev.position() if hasattr(ev, 'position') else ev.localPos()
        if not hasattr(self, 'mousePos'):
            self.mousePos = lpos
        diff = lpos - self.mousePos
        self.mousePos = lpos
        
        if ev.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if (ev.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
                self.pan(diff.x() * 0.05, diff.y() * 0.05, 0, relative='view')
            else:
                self.orbit(-diff.x() * 0.05, diff.y() * 0.05)
        elif ev.buttons() == QtCore.Qt.MouseButton.MiddleButton:
            pass

def spherical_to_cartesian(alt, az, radius=995):
    theta = np.pi / 2 - alt
    x = radius * np.sin(theta) * np.cos(az)
    y = radius * np.sin(theta) * np.sin(az)
    z = radius * np.cos(theta)
    return x, y, z

def create_sphere(r=1005, rows=50, cols=50):
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows, cols, radius=r),
        smooth=True)
    mesh.setColor((0, 0, 0, 1))
    mesh.setGLOptions('opaque')
    return mesh

def create_plane():
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData(vertexes=np.array([
            [-1000, -1000, 0],
            [1000, -1000, 0],
            [1000, 1000, 0],
            [-1000, 1000, 0]
        ]), faces=np.array([
            [0, 1, 2],
            [0, 3, 2]
        ])), smooth=False)
    mesh.setColor((0.2, 0.2, 0.2, 1))
    mesh.setGLOptions('opaque')
    return mesh

def stars(star_data):
    cords, magnitude = [], []
    for star in star_data:
        cords.append(spherical_to_cartesian(star.alt, star.az))
        magnitude.append((-star.magnitude + 7) * 1.2)
    sphere = gl.GLScatterPlotItem(pos=cords, size=magnitude, color=(0.7, 0.7, 1, 1), pxMode=False)
    sphere.setGLOptions('opaque')
    return sphere

def alt_polar_axes(r=1000):
    axis_alt = [gl.GLLinePlotItem(
        pos=np.array(
            [[r*np.cos(np.deg2rad(angle))*float(np.cos(np.pi/72 * a)),
              r*np.cos(np.deg2rad(angle))*float(np.sin(np.pi/72 * a)),
              r*np.sin(np.deg2rad(angle))] 
             for a in np.arange(145)]),
        color=(0.5, 0.5, 0.5, 0.5), width=0.5 if angle == 0 else 0.2) 
        for angle in np.arange(-180,180,10)]
    for circle in axis_alt:
        circle.setGLOptions('opaque')
    return axis_alt

def az_polar_axes(r=1000):
    axis_az = [gl.GLLinePlotItem(
        pos=np.array(
            [[r*np.sin(np.deg2rad(angle))*np.sin(np.pi/72*a), 
              r*np.cos(np.deg2rad(angle))*np.sin(np.pi/72*a), 
              r*np.cos(np.pi/72*a)] 
            for a in np.arange(1, 144)]),
        color=(0.5 if angle % 90 != 0 else 1, 
               0.5 if angle % 90 != 0 else 1, 
               0.5 if angle % 90 != 0 else 1, 1),
        width=0.2 if angle % 90 != 0 else 0.5)
        for angle in np.arange(0, 180, 10)]
    for circle in axis_az:
        circle.setGLOptions('opaque')
    return axis_az

