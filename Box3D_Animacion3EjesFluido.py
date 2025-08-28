# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()
ax = plt.axes(projection = "3d")

def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)

def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth)

def sind(t):
    return np.sin(t*np.pi/180)

def cosd(t):
    return np.cos(t*np.pi/180)

def RotX(t):
    return np.array([[1,0,0],[0,cosd(t),-sind(t)],[0,sind(t),cosd(t)]])

def RotY(t):
    return np.array([[cosd(t),0,sind(t)],[0,1,0],[-sind(t),0,cosd(t)]])

def RotZ(t):
    return np.array([[cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]])

def drawVector(p_fin, p_init=[0,0,0], color='black', linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ, color=color, linewidth=linewidth)

def drawScatter(point, color='black', marker='o'):
    ax.scatter(point[0], point[1], point[2], marker=marker, color=color)

def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='black'):
    drawScatter(p1); drawScatter(p2); drawScatter(p3); drawScatter(p4)
    drawScatter(p5); drawScatter(p6); drawScatter(p7); drawScatter(p8)
    drawVector(p1,p2,color=color); drawVector(p2,p3,color=color)
    drawVector(p3,p4,color=color); drawVector(p4,p1,color=color)
    drawVector(p5,p6,color=color); drawVector(p6,p7,color=color)
    drawVector(p7,p8,color=color); drawVector(p8,p5,color=color)
    drawVector(p4,p8,color=color); drawVector(p1,p5,color=color)
    drawVector(p3,p7,color=color); drawVector(p2,p6,color=color)

def rotate_box(p1,p2,p3,p4,p5,p6,p7,p8, angle_x=0, angle_y=0, angle_z=0):
    # Multiplica las tres matrices de rotación para un giro combinado
    rotation_matrix = RotX(angle_x) @ RotY(angle_y) @ RotZ(angle_z)
    return [rotation_matrix.dot(p) for p in [p1,p2,p3,p4,p5,p6,p7,p8]]

def rotate(steps=90):
    points = [
        np.array([0,0,0]), np.array([7,0,0]), np.array([7,0,3]), np.array([0,0,3]),
        np.array([0,2,0]), np.array([7,2,0]), np.array([7,2,3]), np.array([0,2,3])
    ]

    for n in range(steps):
        ax.cla()
        setaxis(-15,15,-15,15,-15,15)
        fix_system(10,1)

        # rotación simultánea en X, Y y Z
        points_rot = rotate_box(*points, angle_x=n*2, angle_y=n*2, angle_z=n*2)

        drawBox(*points_rot, color='red')
        plt.draw()
        plt.pause(0.05)

# Llamar animación
rotate(90)
plt.draw()
plt.show()
