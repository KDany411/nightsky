import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PySide6.QtCore import QTimer
from PySide6 import QtCore
import sys
import stars

class NoMouseZoom(gl.GLViewWidget):
    """Adjusting the mouse controls inj the 3D view: first disabling all zooming with the mouse wheel,
    then adjusting the mouse movement speed when rotating or panning the view, left mouse button rotates fast,
    right mouse button rotates slow."""
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
                self.pan(diff.x() * 0.2, diff.y() * 0.2, 0, relative='view')
            else:
                self.orbit(-diff.x() * 0.2, diff.y() * 0.2)
        elif ev.buttons() == QtCore.Qt.MouseButton.RightButton:
            if (ev.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier):
                self.pan(diff.x() * 0.03, diff.y() * 0.03, 0, relative='view')
            else:
                self.orbit(-diff.x() * 0.03, diff.y() * 0.03)

def spherical_to_cartesian(alt, az, radius=995):
    """Frequently used conversion from spherical to cartesian coordinates, 
    with adjustment to use the azimuth/altitude convention of angles."""
    theta = np.pi / 2 - alt
    x = radius * np.sin(theta) * np.cos(az)
    y = -radius * np.sin(theta) * np.sin(az)
    z = radius * np.cos(theta)
    return x, y, z

def create_sphere(r=1005, rows=50, cols=50):
    """Generates a sphere mesh, not currently used."""
    mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows, cols, radius=r),
        smooth=True)
    mesh.setColor((0, 0, 0, 1))
    mesh.setGLOptions('opaque')
    return mesh

def create_plane():
    """Generates a horizontal disk mesh representing the horizon plane. Due to no function for a disk mesh in pyqtgraph,
    it is created by generating vertexes in a circular pattern and connecting them to the center in this pizza slice manner."""
    
    # going around and creating points
    list_of_vertexes = np.array([[1000*np.cos(np.deg2rad(angle)),1000*np.sin(np.deg2rad(angle)),0] 
                                 for angle in np.arange(0, 360, 3)])
    
    # tehn adding the middle one
    list_of_vertexes = np.vstack((list_of_vertexes, np.array([0,0,0])))
    mesh = gl.GLMeshItem(meshdata=gl.MeshData(
                        vertexes=list_of_vertexes, 
                        faces=np.array([[0, i, i+1] for i in range(1, 119)]), 
                        faceColors=np.array([[0, 0.1, 0, 0.5] for i in range(119)])))
    mesh.setGLOptions('opaque')
    return mesh

def create_stars(star_data):
    """Plots the stars from the data on a sphere with radius 995, converting the spherical horizontal coordinates to cartesian.
    The size of each star is determined by its magnitude by a tuned formula"""
    cords, magnitude = [], []
    
    # the number of visible stars can be adjusted in the parametrs of a function in stars.py
    for star in star_data:
        cords.append(spherical_to_cartesian(star.alt, star.az))
        magnitude.append((-star.magnitude + 7) * 1.2)
    sphere = gl.GLScatterPlotItem(pos=cords, size=magnitude, color=(0.7, 0.7, 1, 1), pxMode=False)
    sphere.setGLOptions('opaque')
    return sphere

def alt_polar_axes(r=1000):
    """Using line plots to create the altitude coordinate lines, every 10 degrees from -180 to 170,
    each "ring" is made as a seperate mesh item so it can be generated using a simple formula"""
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
    """Using line plots to create the azimuth coordinate lines, every 10 degrees from 0 to 170,
    here the seperate rigs allow me to make the main directions (N, E, S, W) thicker and brighter"""
    axis_az = [gl.GLLinePlotItem(
        pos=np.array(
            [[r*np.sin(np.deg2rad(angle))*np.sin(np.pi/72*a), 
              r*np.cos(np.deg2rad(angle))*np.sin(np.pi/72*a), 
              r*np.cos(np.pi/72*a)] 
            for a in np.arange(0, 145)]),
        # had to resort to this ungly thing 
        color=(0.5 if angle % 90 != 0 else 1, 
               0.5 if angle % 90 != 0 else 1, 
               0.5 if angle % 90 != 0 else 1, 1),
        width=0.2 if angle % 90 != 0 else 0.5)
        for angle in np.arange(0, 180, 10)]
    for circle in axis_az:
        circle.setGLOptions('opaque')
    return axis_az

def sun(sun_position):
    """Sphere for the sun"""
    alt, az = sun_position
    x, y, z = spherical_to_cartesian(alt, az, radius=990)
    sun_mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows=20, cols=20, radius=17.45),
        smooth=True,
        color=(1, 1, 0, 1))
    sun_mesh.translate(x, y, z)
    sun_mesh.setGLOptions('opaque')
    return sun_mesh

def moon(moon_position):
    """And the moon"""
    alt, az = moon_position
    x, y, z = spherical_to_cartesian(alt, az, radius=990)
    moon_mesh = gl.GLMeshItem(
        meshdata=gl.MeshData.sphere(rows=20, cols=20, radius=17.45),
        smooth=True,
        color=(0.9, 0.9, 0.9, 1))
    moon_mesh.translate(x, y, z)
    moon_mesh.setGLOptions('opaque')
    return moon_mesh
    
def rotate_around_vec(vec, point, angle):
    """This functions allows me to rotate a point around any given vector defined by spherical coordinates (alt, az).
    I'm using Gram-Schmidt process to create an orthonormal basis with the rotation vector as the first vector of the basis,
    then applying a rotation matrix around the first basis vector and transforming back to the standard basis.
    This is used to create the equatorial coordinate lines."""
    
    # get the carthesian vector from its angle and normalize
    vec1_ = np.array(spherical_to_cartesian(vec[0], vec[1]))
    vec1 = vec1_ / np.linalg.vector_norm(vec1_)
    
    # pick a random point that is independent from the vec1 one
    u = np.array([200,1000,300])
    
    # Gram-Schmdt
    vec2_ =  u - np.dot(u, vec1) * vec1
    vec2 = vec2_ / np.linalg.vector_norm(vec2_)
    
    # 3rd vector found using the cross product of the two before
    vec3 = np.cross(vec1, vec2)/np.linalg.vector_norm(np.cross(vec1, vec2))
    
    # base change matrix and its inverse
    base = np.array([vec1, vec2, vec3]).T
    base_inverse = np.linalg.inv(base)
    
    # and the rotation matrix
    rot = np.array([[1,0,0],[0,np.cos(angle),np.sin(angle)],[0,-np.sin(angle),np.cos(angle)]])
    
    rotated = base @ rot @ base_inverse @ np.array(point)
    return rotated

def dec_polar_axis(r=1000):
    """Generates the declination coordinate lines, every 10 degrees from 0 to 170,
    using the rotate_around_vec function to create rings around the celestial pole.
    The celestial pole position is obtained from stars.py"""
    pole_alt, pole_az = stars.get_radec_pole_position()
    pole_alt_deg = np.rad2deg(pole_alt)
    axis_dec = []
    
    # here i am creating rings by rotating one point around the axis vector
    for angle in np.arange(0, 180, 10):
        points = []
        for a in np.arange(0, 361, 3):
            point = np.array([rotate_around_vec(
                            (pole_alt, pole_az), 
                            spherical_to_cartesian(np.deg2rad(pole_alt_deg-angle),pole_az), 
                            np.deg2rad(a))])
            norm = np.linalg.norm(point)
            points.append(point)
            
        axis_dec.append(
                    gl.GLLinePlotItem(
                    pos=points,
                    color=(0.7 if angle == 90 else 0.5, 
                           0.5 if angle == 90 else 0.3, 
                           0.5 if angle == 90 else 0.3, 0.5),
                    width=0.8 if angle == 90 else 0.4))
        
    for line in axis_dec: line.setGLOptions('opaque')
    return axis_dec

def ra_polar_axis(r=1000):
    """Generates the right ascension coordinate lines, every 10 degrees from 0 to 170,
    I had to use a more complex approach here, first creating a reference ring that goes through the 0hr RA line and the celestial pole,
    Then I generated rings from this reference ring by rootating it by 10 degrees at a time.
    
    To find the reference ring I had to first find out what is the right ascension of a point directly below the pole,
    then generate a reference ring that goes through the the celestial pole and the zenith (similarly to the azimuth rings),
    then I had to rotate this reference ring by the angle that coresponds to the point below the pole.
    Now the reference ring matched the 0hr RA line so I was able to generate the rest"""
    pole_alt, pole_az = stars.get_radec_pole_position()
    axis_ra, reference_ring = [], []
    
    # reference ring with all the shenanigans
    for a in np.arange(0, 145):
            reference_ring.append(np.array(rotate_around_vec(
                                (pole_alt, pole_az),
                                [r*np.sin(pole_az + np.pi/2)*np.sin(np.pi/72*a), 
                                r*np.cos(pole_az + np.pi/2)*np.sin(np.pi/72*a), 
                                r*np.cos(np.pi/72*a)], 
                                stars.get_ra_angle())))

    for angle in np.arange(0, 180, 10):
        current_ring = []
        
        # generating using the reference ring
        for point in reference_ring:
            rotated_point = rotate_around_vec((pole_alt, pole_az), point, np.deg2rad(angle))
            current_ring.append(rotated_point)
        axis_ra.append(
                    gl.GLLinePlotItem(
                    pos=current_ring,
                    color=(0.7 if angle % 90 == 0 else 0.5, 
                           0.5 if angle % 90 == 0 else 0.3, 
                           0.5 if angle % 90 == 0 else 0.3, 0.5),
                    width=0.8 if angle % 90 == 0 else 0.4))    
        
    for line in axis_ra: line.setGLOptions('opaque')
    return axis_ra
        
        
            
                
        