# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
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
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)

def sind(t):
    return np.sin(t*np.pi/180)

def cosd(t):
    return np.cos(t*np.pi/180)

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)

def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color = 'black'):
    drawScatter(p1)
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    drawVector(p1,p2,color = color)
    drawVector(p2,p3,color = color)
    drawVector(p3,p4,color = color)
    drawVector(p4,p1,color = color)
    drawVector(p5,p6,color = color)
    drawVector(p6,p7,color = color)
    drawVector(p7,p8,color = color)
    drawVector(p8,p5,color = color)
    drawVector(p4,p8,color = color)
    drawVector(p1,p5,color = color)
    drawVector(p3,p7,color = color)
    drawVector(p2,p6,color = color)

def drawScatter(point,color='black',marker='o'):
    ax.scatter(point[0],point[1],point[2],marker='o')

# ============================================================
# 🔥 NUEVA FUNCIÓN: traslación + rotación homogénea
# ============================================================
def move_and_rotate_Box(p1,p2,p3,p4,p5,p6,p7,p8, delta_x=0, delta_y=0, delta_z=0, theta=0, axis='z'):
    # Puntos en forma homogénea
    points = [np.array([p[0], p[1], p[2], 1]) for p in [p1,p2,p3,p4,p5,p6,p7,p8]]

    # Matriz de traslación
    T = np.array([[1,0,0,delta_x],
                  [0,1,0,delta_y],
                  [0,0,1,delta_z],
                  [0,0,0,1]])

    # Matriz de rotación homogénea
    if axis=='z':
        R = np.array([[cosd(theta), -sind(theta), 0, 0],
                      [sind(theta),  cosd(theta), 0, 0],
                      [0,            0,           1, 0],
                      [0,            0,           0, 1]])
    elif axis=='x':
        R = np.array([[1, 0,          0,           0],
                      [0, cosd(theta),-sind(theta),0],
                      [0, sind(theta), cosd(theta),0],
                      [0, 0,          0,           1]])
    elif axis=='y':
        R = np.array([[cosd(theta), 0, sind(theta),0],
                      [0,           1, 0,          0],
                      [-sind(theta),0, cosd(theta),0],
                      [0,           0, 0,          1]])
    else:
        R = np.eye(4)  # identidad por defecto

    # Matriz de transformación compuesta (rotación + traslación)
    M = T @ R  

    # Transformar cada punto
    transformed_points = [M.dot(p)[:3] for p in points]

    return transformed_points

# ============================================================
# MAIN
# ============================================================

# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,1)

# Caja original
p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]

# Caja original dibujada
drawBox(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init)

# Caja trasladada + rotada
box_transformed = move_and_rotate_Box(p1_init, p2_init, p3_init, p4_init,
                                      p5_init, p6_init, p7_init, p8_init,
                                      delta_x=4, delta_y=4, delta_z=4,
                                      theta=45, axis='z')

drawBox(*box_transformed)

# show image
plt.draw()
plt.show()
