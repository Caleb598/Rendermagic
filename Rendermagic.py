import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL import GLUT as glut  # Import the GLUT module
import tkinter as tk
from math import pi, cos, sin
import time
import math
import os
from PIL import Image
import cv2
import numpy as np

# Initialize GLFW
if not glfw.init():
    raise RuntimeError("Failed to initialize GLFW")

# Global variables for camera position and rotation
camera_pos = [3, 4, 5]
camera_rot = [0, 0, 0]
camera_speed = 0.1
zoom_speed = 0.1
last_x, last_y = 0, 0
left_mouse_button_pressed = False

class Keyframe:
    def __init__(self, frame, position, rotation):
        self.frame = frame
        self.position = position
        self.rotation = rotation

class Camera:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
        self.keyframes = []

    def add_keyframe(self, frame, position, rotation):
        keyframe = Keyframe(frame, position, rotation)
        self.keyframes.append(keyframe)

    def update_from_keyframes(self, elapsed_time):
        for i in range(len(self.keyframes) - 1):
            if self.keyframes[i].frame <= elapsed_time <= self.keyframes[i + 1].frame:
                t = (elapsed_time - self.keyframes[i].frame) / (self.keyframes[i + 1].frame - self.keyframes[i].frame)
                self.position = self.interpolate(self.position, self.keyframes[i + 1].position, t)
                self.rotation = self.interpolate(self.rotation, self.keyframes[i + 1].rotation, t)
                break
        
    def interpolate(self, start, end, t):
        return [start[j] + (end[j] - start[j]) * t for j in range(len(start))]

# Global variables for camera properties
camera = Camera(position=[5, 5, 5], rotation=[0, 0, 0])

# Function to update camera from keyframes
def update_camera(elapsed_time):
    camera.update_from_keyframes(elapsed_time)

# Keyframes for camera
camera.add_keyframe(frame=0, position=[5, 5, 5], rotation=[0, 0, 0])
camera.add_keyframe(frame=50, position=[3, 4, 5], rotation=[45, 45, 0])

# List to store animation frames
animation_frames = []

# List to store objects in the scene
objects = []

# Declare global variables at the beginning of your script
window = None
background_color = [0.0, 1.0, 1.0]

# Global variables for light properties
light1_position = [5.0, 5.0, 5.0, 25.0]  # Light 1 position
light1_ambient = [0.2, 0.2, 0.2, 1.0]     # Ambient light 1 color
light1_diffuse = [0.8, 0.8, 0.8, 1.0]     # Diffuse light 1 color
light1_specular = [1.0, 1.0, 1.0, 1.0]    # Specular light 1 color

# Function to enable lighting and set up light parameters
def setup_lighting():
    glEnable(GL_LIGHTING)
    
    # Light 1
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light1_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light1_specular)

    glEnable(GL_COLOR_MATERIAL)

class Keyframe:
    def __init__(self, frame, position, ambient, diffuse, specular):
        self.frame = frame
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

class GameObject:
    def __init__(self, position, ambient, diffuse, specular):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.keyframes = []

    def add_keyframe(self, frame, position, ambient, diffuse, specular):
        keyframe = Keyframe(frame, position, ambient, diffuse, specular)
        self.keyframes.append(keyframe)

    def update_from_keyframes(self, elapsed_time):
        for i in range(len(self.keyframes) - 1):
            if self.keyframes[i].frame <= elapsed_time <= self.keyframes[i + 1].frame:
                t = (elapsed_time - self.keyframes[i].frame) / (self.keyframes[i + 1].frame - self.keyframes[i].frame)
                self.position = self.interpolate(self.keyframes[i].position, self.keyframes[i + 1].position, t)
                self.ambient = self.interpolate(self.keyframes[i].ambient, self.keyframes[i + 1].ambient, t)
                self.diffuse = self.interpolate(self.keyframes[i].diffuse, self.keyframes[i + 1].diffuse, t)
                self.specular = self.interpolate(self.keyframes[i].specular, self.keyframes[i + 1].specular, t)
                break

    def interpolate(self, start, end, t):
        return [start[j] + (end[j] - start[j]) * t for j in range(len(start))]

# Global variables for light properties
light1 = GameObject([5.0, 5.0, 5.0, 20.0], [0.2, 0.2, 0.2, 1.0], [0.8, 0.8, 0.8, 1.0], [1.0, 1.0, 1.0, 1.0])

# Function to update lights from keyframes
def update_lights(elapsed_time):
    light1.update_from_keyframes(elapsed_time)
    glEnable(GL_LIGHTING)
    
    # Light 1
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light1.position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light1.ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light1.diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light1.specular)

# Keyframes for lights
light1.add_keyframe(frame=0, position=[5.0, 5.0, 5.0, 20.0], ambient=[0.2, 0.2, 0.2, 1.0], diffuse=[0.8, 0.8, 0.8, 1.0], specular=[1.0, 1.0, 1.0, 1.0])
light1.add_keyframe(frame=50, position=[-5.0, -5.0, -5.0, 20.0], ambient=[0.1, 0.1, 0.1, 1.0], diffuse=[0.5, 0.5, 0.5, 1.0], specular=[0.8, 0.8, 0.8, 1.0])

# Function to set up material properties
def setup_material():
    ambient_color = [0.2, 0.2, 0.2, 1.0]
    diffuse_color = [0.8, 0.8, 0.8, 1.0]
    specular_color = [1.0, 1.0, 1.0, 1.0]

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient_color)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse_color)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_color)
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def setup_transparency(alpha):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_ALPHA_TEST)
    glAlphaFunc(GL_GREATER, 0.1)  # Adjust the alpha threshold as needed
    glColor4f(1.0, 1.0, 1.0, alpha)

# Function to draw a colored cube with more realistic shading
def draw_realistic_cube(position, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
      
    glBegin(GL_QUADS)
    
    glColor4fv(color)

    glNormal3f(0, 0, -1)
    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] - 0.5)
    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] - 0.5)

    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] + 0.5)
    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] + 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] + 0.5)

    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] + 0.5)
    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] + 0.5)

    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] + 0.5)

    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] - 0.5)
    glVertex3f(position[0] - 0.5, position[1] + 0.5, position[2] + 0.5)
    glVertex3f(position[0] - 0.5, position[1] - 0.5, position[2] + 0.5)

    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] - 0.5)
    glVertex3f(position[0] + 0.5, position[1] + 0.5, position[2] + 0.5)
    glVertex3f(position[0] + 0.5, position[1] - 0.5, position[2] + 0.5)

    glEnd()

def draw_realistic_sphere(position, radius=0.5, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
    
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])

    glColor4fv(color)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, radius, 100, 100)

    glPopMatrix()

# Function to draw a colored cylinder with tops (caps) and more realistic shading
def draw_realistic_cylinder(position, radius=0.5, height=1.0, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
    
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glRotatef(90, 1, 0, 0)  # Rotate to align the cylinder with the y-axis

    glColor4fv(color)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

    # Draw top cap
    gluDisk(quad, 0, radius, 100, 1)
    
    # Draw cylinder body
    gluCylinder(quad, radius, radius, height, 100, 100)

    # Draw bottom cap
    glTranslatef(0, 0, height)
    gluDisk(quad, 0, radius, 100, 1)

    glPopMatrix()

# Function to draw a colored cone with a flat bottom and more realistic shading
def draw_realistic_cone(position, radius=0.5, height=1.0, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
    
    glPushMatrix()
    glTranslatef(position[0], position[1] - 0.5 * height, position[2])  # Adjusted translation
    glRotatef(-90, 1, 0, 0)  # Rotate to align the cone with the y-axis

    glColor4fv(color)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

    # Draw cone body
    gluCylinder(quad, radius, 0, height, 100, 100)  # Set the top radius to 0

    glPopMatrix()

def draw_2d_plane(size=1.0, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
    
    glBegin(GL_QUADS)
    glColor4fv(color)

    glVertex3f(-size / 2, -size / 2, 0.0)  # Bottom-left corner
    glVertex3f(size / 2, -size / 2, 0.0)   # Bottom-right corner
    glVertex3f(size / 2, size / 2, 0.0)    # Top-right corner
    glVertex3f(-size / 2, size / 2, 0.0)   # Top-left corner

    glEnd()

def draw_realistic_torus(position, inner_radius=0.2, outer_radius=0.4, color=(1.0, 1.0, 1.0, 1.0)):
    setup_material()
    
    setup_transparency(color[3])  # Set up transparency
    
    glColor4fv(color)

    num_slices = 100
    num_segments = 100

    for i in range(num_slices):
        phi = 2 * pi * i / num_slices
        cos_phi = cos(phi)
        sin_phi = sin(phi)

        glBegin(GL_QUAD_STRIP)
        for j in range(num_segments + 1):
            theta = 2 * pi * j / num_segments
            cos_theta = cos(theta)
            sin_theta = sin(theta)

            x = (outer_radius + inner_radius * cos_phi) * cos_theta
            y = (outer_radius + inner_radius * cos_phi) * sin_theta
            z = inner_radius * sin_phi

            glNormal3f(cos_theta * cos_phi, sin_theta * cos_phi, sin_phi)
            glVertex3f(position[0] + x, position[1] + y, position[2] + z)

            x = (outer_radius + inner_radius * cos((i + 1) * 2 * pi / num_slices)) * cos_theta
            y = (outer_radius + inner_radius * cos((i + 1) * 2 * pi / num_slices)) * sin_theta
            z = inner_radius * sin((i + 1) * 2 * pi / num_slices)

            glNormal3f(cos_theta * cos((i + 1) * 2 * pi / num_slices), sin_theta * cos((i + 1) * 2 * pi / num_slices), sin((i + 1) * 2 * pi / num_slices))
            glVertex3f(position[0] + x, position[1] + y, position[2] + z)

        glEnd()

def update_shape(shape_draw_function):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    shape_draw_function()
    glutSwapBuffers()

class GameObject:
    def __init__(self, position, rotation, scale, color, texture=None, emission=1.0,
                 metallic=0.0, roughness=1.0, specular=[1.0, 1.0, 1.0, 1.0],
                 subsurface=0.0, specular_tint=[1.0, 1.0, 1.0, 1.0],
                 anisotropy=0.0, sheen=0.0, sheen_tint=[1.0, 1.0, 1.0, 1.0],
                 clearcoat=0.0, clearcoat_gloss=0.0, normal_map=None):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.texture = texture
        self.emission = max(0.0, emission)  # Ensure emission is at least 0
        self.metallic = metallic
        self.roughness = roughness
        self.specular = specular
        self.subsurface = subsurface
        self.specular_tint = specular_tint
        self.anisotropy = anisotropy
        self.sheen = sheen
        self.sheen_tint = sheen_tint
        self.clearcoat = clearcoat
        self.clearcoat_gloss = clearcoat_gloss
        self.normal_map = normal_map
        self.keyframes = {
            'position': [],
            'rotation': [],
            'scale': [],
            'color': [],
        }
    
    def add_keyframe(self, frame, **kwargs):
        keyframe = {'frame': frame, **kwargs}
        for prop in self.keyframes.keys():
            if prop in kwargs:
                self.keyframes[prop].append(keyframe)

    def interpolate_keyframes(self, keyframe1, keyframe2, t):
        interpolated_keyframe = {}
        for prop in keyframe1.keys():
            if prop in keyframe2 and keyframe1[prop] is not None and keyframe2[prop] is not None:
                interpolated_keyframe[prop] = self.interpolate(keyframe1[prop], keyframe2[prop], t)
        return interpolated_keyframe

    def update_from_keyframes(self, current_frame):
        for prop in self.keyframes.keys():
            if prop != 'frame' and self.keyframes[prop]:
                keyframe1, keyframe2 = self.find_keyframes(self.keyframes[prop], current_frame)
                if keyframe1 and keyframe2:
                    t = self.calculate_interpolation_parameter(current_frame, keyframe1['frame'], keyframe2['frame'])
                    interpolated_value = self.interpolate_keyframes(keyframe1, keyframe2, t)[prop]
                    setattr(self, prop, interpolated_value)

    def update_color(self, current_frame, t):
        # Initialize color with the default color
        color = self.color[:]

        # Interpolate color if keyframes exist
        if self.keyframes['color']:
            keyframe1, keyframe2 = self.find_keyframes(self.keyframes['color'], current_frame)
            if keyframe1 and keyframe2:
                t = self.calculate_interpolation_parameter(current_frame, keyframe1['frame'], keyframe2['frame'])
                interpolated_color = self.interpolate_keyframes(keyframe1, keyframe2, t)['color']
                color = interpolated_color

    @staticmethod
    def find_keyframes(keyframes, current_frame):
        keyframe1, keyframe2 = None, None
        for keyframe in keyframes:
            if keyframe['frame'] <= current_frame:
                keyframe1 = keyframe
            elif keyframe['frame'] > current_frame:
                keyframe2 = keyframe
                break
        return keyframe1, keyframe2

    @staticmethod
    def calculate_interpolation_parameter(current_frame, frame1, frame2):
        total_frames = frame2 - frame1
        if total_frames == 0:
            return 0.0
        return (current_frame - frame1) / total_frames

    @staticmethod
    def interpolate(value1, value2, t):
        if isinstance(value1, list) and isinstance(value2, list):
            return [v1 + (v2 - v1) * t for v1, v2 in zip(value1, value2)]
        else:
            return value1 + (value2 - value1) * t

# Create instances for each object with textures
torus1 = GameObject([-4, 0, -2], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 1.0, 1.0])
torus2 = GameObject([4, 0, -2], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0])
plane1 = GameObject([0, -2, 0], [90.0, 0.0, 0.0], [2.5, 2.5, 2.5], [1.0, 0.4, 0.0, 1.0])
plane2 = GameObject([2, 0, -2], [0.0, 0.0, 0.0], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 1.0])
cone1 = GameObject([0, 0, -2], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0])
cone2 = GameObject([0, 0, 2], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.8, 0.0, 1.0])
cylinder1 = GameObject([-4, 0.5, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0])
cylinder2 = GameObject([4, 0.5, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.8, 1.0])
sphere1 = GameObject([2, 0, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0, 1.0])
sphere2 = GameObject([-2, 0, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 0.8, 0.0, 1.0])
cube1 = GameObject([0, 0, 0], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [1.0, 0.0, 0.0, 1.0])
cube2 = GameObject([0, 0, -4], [0.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.8, 0.0, 0.0, 1.0])

# Add keyframes for animation
torus1.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[-4, 0, -2], scale=[1.0, 1.0, 1.0], color=[1.0, 0.0, 1.0, 1.0])
torus1.add_keyframe(frame=50, rotation=[180.0, 0.0, 0.0], position=[4, 0, -2], scale=[1.0, 1.0, 1.0], color=[0.0, 1.0, 1.0, 1.0])
torus2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[4, 0, -2], scale=[1.0, 1.0, 1.0], color=[0.0, 1.0, 1.0, 1.0])
torus2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[-4, 0, -2], scale=[1.0, 1.0, 1.0], color=[0.0, 1.0, 1.0, 1.0])
plane2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[2, 0, -2], scale=[0.5, 0.5, 0.5], color=[0.5, 0.5, 0.5, 1.0])
plane2.add_keyframe(frame=50, rotation=[90.0, 0.0, 0.0], position=[-2, 0, -2], scale=[1.0, 1.0, 1.0], color=[1.0, 0.4, 0.0, 1.0])
cone1.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[0, 0, -2], scale=[1.0, 1.0, 1.0], color=[1.0, 1.0, 0.0, 1.0])
cone1.add_keyframe(frame=50, rotation=[180.0, 0.0, 0.0], position=[0, 0, 2], scale=[1.0, 1.0, 1.0], color=[1.0, 0.0, 0.0, 1.0])
cone2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[0, 0, 2], scale=[1.0, 1.0, 1.0], color=[1.0, 0.8, 0.0, 1.0])
cone2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[0, 0, -2], scale=[1.0, 1.0, 1.0], color=[1.0, 1.0, 0.0, 1.0])
cylinder1.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[-4, 0.5, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.0, 1.0, 1.0])
cylinder1.add_keyframe(frame=50, rotation=[180.0, 0.0, 0.0], position=[4, 0.5, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.0, 0.8, 1.0])
cylinder2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[4, 0.5, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.0, 0.8, 1.0])
cylinder2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[-4, 0.5, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.0, 0.8, 1.0])
sphere1.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[2, 0, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 1.0, 0.0, 1.0])
sphere1.add_keyframe(frame=50, rotation=[180.0, 0.0, 0.0], position=[-2, 0, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.8, 0.0, 1.0])
sphere2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[-2, 0, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 0.8, 0.0, 1.0])
sphere2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[2, 0, 0], scale=[1.0, 1.0, 1.0], color=[0.0, 1.0, 0.0, 1.0])
cube1.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[0, 0, 0], scale=[1.0, 1.0, 1.0], color=[1.0, 0.0, 0.0, 1.0])
cube1.add_keyframe(frame=50, rotation=[180.0, 0.0, 0.0], position=[0, 0, -4], scale=[1.0, 1.0, 1.0], color=[0.8, 0.0, 0.0, 1.0])
cube2.add_keyframe(frame=1, rotation=[0.0, 0.0, 0.0], position=[0, 0, -4], scale=[1.0, 1.0, 1.0], color=[0.8, 0.0, 0.0, 1.0])
cube2.add_keyframe(frame=50, rotation=[0.0, 180.0, 0.0], position=[0, 0, 0], scale=[1.0, 1.0, 1.0], color=[1.0, 0.0, 0.0, 1.0])

def update_animation():
    global current_frame
    elapsed_time = time.time() - start_animation_time
    for obj in [torus1, torus2, plane1, plane2, cone1, cone2, cylinder1, cylinder2, sphere1, sphere2, cube1, cube2]:
        obj.update_from_keyframes(current_frame)
        
# Set up cube parameters
cube_position = [0, 0, 0]
cube_scale = 1.0

# Global variables for time and animation
start_animation_time = time.time()
current_frame = 0
end_frame = 50  # Set the end frame for your animation

total_render_time = 0.0
printed_total_time = False
render_time_printed = False  # Flag to track if render time has been printed

# Directory to save frames
frame_directory = "frames"

window_width = 1920
window_height = 1080

# Global variable for start time of rendering
start_render_time = None

# Define render_complete global variable
render_complete = False
start_render_time = time.time()  # Initialize start_render_time here or wherever appropriate

def draw_scene(save_frame=True):
    global window, background_color, current_frame, total_render_time, printed_total_time, render_time_printed, start_render_time, render_complete

    # Initialize render_complete if it's None
    if render_complete is None:
        render_complete = False

    # Check if rendering is complete
    if render_complete:
        return

    # Record the start time for each frame
    start_time = time.time()

    # Update camera from keyframes
    elapsed_time = time.time() - start_animation_time
    camera.update_from_keyframes(elapsed_time)

    glClearColor(background_color[0], background_color[1], background_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up camera
    glLoadIdentity()
    gluLookAt(camera.position[0], camera.position[1], camera.position[2], 0, 0, 0, 0, 1, 0)

    # Apply camera rotation
    glRotatef(camera.rotation[0], 1, 0, 0)
    glRotatef(camera.rotation[1], 0, 1, 0)
    glRotatef(camera.rotation[2], 0, 0, 1)

    # Check if rendering is complete after each frame
    if current_frame >= end_frame:
        render_complete = True

    # Enable lighting and set light parameters
    setup_lighting()

    # Enable smooth shading
    glShadeModel(GL_SMOOTH)

    # Reset modelview matrix before applying local transformations
    glPushMatrix()

    for obj in [torus1, torus2, plane1, plane2, cone1, cone2, cylinder1, cylinder2, sphere1, sphere2, cube1, cube2]:
        # Save the current matrix state
        glPushMatrix()

        # Apply object transformations
        glTranslatef(obj.position[0], obj.position[1], obj.position[2])
        glRotatef(obj.rotation[0], 1, 0, 0)
        glRotatef(obj.rotation[1], 0, 1, 0)
        glRotatef(obj.rotation[2], 0, 0, 1)
        glScalef(obj.scale[0], obj.scale[1], obj.scale[2])
        
        # Draw the object
        if obj == torus1 or obj == torus2:
            draw_realistic_torus([0, 0, 0], inner_radius=0.2, outer_radius=0.5, color=obj.color)
        elif obj == plane1 or obj == plane2:
            draw_2d_plane(size=2.0, color=obj.color)
        elif obj == cone1 or obj == cone2:
            draw_realistic_cone([0, 0, 0], radius=0.5, height=1.0, color=obj.color)
        elif obj == cylinder1 or obj == cylinder2:
            draw_realistic_cylinder([0, 0, 0], radius=0.5, height=1.0, color=obj.color)
        elif obj == sphere1 or obj == sphere2:
            draw_realistic_sphere([0, 0, 0], radius=0.5, color=obj.color)
        elif obj == cube1 or obj == cube2:
            draw_realistic_cube([0, 0, 0], color=obj.color)

        # Restore the saved matrix state
        glPopMatrix()

    # Restore the modelview matrix
    glPopMatrix()

    # Swap buffers
    glfw.swap_buffers(window)

    # Record the end time
    end_time = time.time()

    # Calculate the total time elapsed
    total_time = end_time - start_time

    # Print the current frame and render time
    if current_frame <= end_frame:
        print(f"Frame {current_frame} Render Time Elapsed: {total_time // 60:02.0f}:{total_time % 60:05.2f}")

    # Increment the total render time
    total_render_time += total_time

    # Save frame if requested and if the animation is ongoing
    if save_frame and current_frame <= end_frame:
        save_frame_to_disk(window_width, window_height, current_frame)

    # Increment the current frame
    current_frame += 1

    # Check if it's the last frame and render time has not been printed yet
    if current_frame > end_frame and not printed_total_time:
        # Ensure start_render_time is initialized
        if start_render_time is not None:
            # Print total render time
            end_render_time = time.time()
            total_render_time = end_render_time - start_render_time
            print(f"Total Render Time Elapsed: {total_render_time // 60:02.0f}:{total_render_time % 60:05.2f}")
            printed_total_time = True
        else:
            print("Error: start_render_time is not initialized.")

def save_frame_to_disk(window_width, window_height, frame_number):
    global frame_directory

    # Create directory if it doesn't exist
    if not os.path.exists(frame_directory):
        os.makedirs(frame_directory)

    # Save the current frame to disk
    filename = os.path.join(frame_directory, f"frame_{frame_number:05d}.png")
    glReadBuffer(GL_FRONT)
    data = glReadPixels(0, 0, window_width, window_height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (window_width, window_height), data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(filename)

def export_frames_to_mp4(frame_directory, frames_per_second):
    # List all frame files and sort them numerically
    frame_files = sorted(os.listdir(frame_directory), key=lambda x: int(x.split('_')[1].split('.')[0]))

    if not frame_files:
        print("No frame files found.")
        return

    # Initialize video writer
    first_frame_path = os.path.join(frame_directory, frame_files[0])
    first_frame = cv2.imread(first_frame_path)
    if first_frame is None:
        print(f"Failed to read the first frame: {first_frame_path}")
        return

    height, width, layers = first_frame.shape

    # Define the path to the "Videos" directory
    videos_directory = os.path.join(os.path.expanduser('~'), 'Videos')

    # Specify the full path for the MP4 file in the "Videos" directory
    mp4_path = os.path.join(videos_directory, "animation.mp4")

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(mp4_path, fourcc, frames_per_second, (width, height))

    # Write frames to video
    for frame_file in frame_files:
        frame_path = os.path.join(frame_directory, frame_file)
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f"Failed to read frame: {frame_file}")
            continue
        video_writer.write(frame)

    # Release video writer
    video_writer.release()

# Example usage
frame_directory = "frames"
frames_per_second = 24.0
export_frames_to_mp4(frame_directory, frames_per_second)

# Render each frame explicitly and save them
def render_and_save_frames(window_width, window_height, end_frame):
    for frame_number in range(1, end_frame + 1):
        # Clear the buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the scene for the current frame
        draw_scene(save_frame=True, current_frame=frame_number)

        # Save the current frame
        save_frame_to_disk(window_width, window_height, frame_number)

def main():
    # Render and save frames
    render_and_save_frames(window_width, window_height, end_frame)

    # Export frames to MP4
    export_frames_to_mp4(frame_directory, frames_per_second)

# Initialize GLFW and create the window
if not glfw.init():
    exit()

# Set window size
width, height = 1920, 1080

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(width, height, "Rendermagic", None, None)

# Function to handle keyboard input
def key_callback(_, key, __, action, ___):
    if action == glfw.PRESS:
        key = chr(key).lower()
        if key in ["w", "s", "a", "d"]:
            update_camera_position(key)

if not window:
    glfw.terminate()
    exit()

# Make the window's context current
glfw.make_context_current(window)

# Draw the scene with the specified background color
draw_scene()

# Set up OpenGL
glEnable(GL_DEPTH_TEST)

# Set up perspective projection matrix with an increased field of view (60 degrees)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60, (width / height), 0.1, 100.0)

glMatrixMode(GL_MODELVIEW)

# Set the callback functions
glfw.set_key_callback(window, key_callback)

# Rendering loop
while not glfw.window_should_close(window):
    # Poll for and process events
    glfw.poll_events()
    
    # Update animation parameters for the current frame
    update_animation()

    # Draw the scene with the specified background color
    draw_scene()

    # Set the camera position based on user input or other logic
    # update_camera_position()

# Render frames and view animation playback
while not glfw.window_should_close(window):
    draw_scene()
    glfw.poll_events()

# Main loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    draw_scene()
    root.update()

# Terminate GLFW and close the Tkinter window when exiting
glfw.terminate()
