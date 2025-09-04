# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")



def setaxis(x1, x2, y1, y2, z1, z2):
    # this function is used to fix the view to the values of input arguments
    # -----------------------------------------------------------------------
    # ARGUMENTS
    # x1, x2 -> numeric value
    # y1, y2 -> numeric value
    # y1, z2 -> numeric value
    # -----------------------------------------------------------------------
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):
    # Fix system function 
    # Plots a 3D centered at [x,y,z] = [0,0,0]
    # -------------------------------------------------------------------
    # Arguments 
    # axis_length -> used to specify the length of the axis, in this case
    #                all axes are of the same length
    # -------------------------------------------------------------------
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)
    

def sind(t):
    # sind function
    # Computes the sin() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
    # sind function
    # Computes the cos() trigonometric function in degrees
    # ----------------------------------------------------------------------
    # Arguments
    # t -> Numeric, angle in degrees. 
    # ----------------------------------------------------------------------
    res = np.cos(t*np.pi/180)
    return res


def RotZ(t):
    Rz = np.array(([cosd(t),-sind(t),0],[sind(t),cosd(t),0],[0,0,1]))
    return Rz

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

#DE AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

def move_Box(p1,p2,p3,p4,p5,p6,p7,p8, delta_x = 0, delta_y = 0, delta_z = 0):
    
    
    p1 = [p1[0], p1[1], p1[2], 1]
    p2 = [p2[0], p2[1], p2[2], 1]
    p3 = [p3[0], p3[1], p3[2], 1]
    p4 = [p4[0], p4[1], p4[2], 1]
    p5 = [p5[0], p5[1], p5[2], 1]
    p6 = [p6[0], p6[1], p6[2], 1]
    p7 = [p7[0], p7[1], p7[2], 1]
    p8 = [p8[0], p8[1], p8[2], 1]


    Translation_Matrix = np.array(([1,0,0, delta_x],[0, 1, 0, delta_y],[0, 0, 1, delta_z],[0, 0, 0, 1]))


    p1_t = Translation_Matrix.dot(p1)
    p2_t = Translation_Matrix.dot(p2)
    p3_t = Translation_Matrix.dot(p3)
    p4_t = Translation_Matrix.dot(p4)
    p5_t = Translation_Matrix.dot(p5)
    p6_t = Translation_Matrix.dot(p6)
    p7_t = Translation_Matrix.dot(p7)
    p8_t = Translation_Matrix.dot(p8)

    p1_t = p1_t[:3]
    p2_t = p2_t[:3]
    p3_t = p3_t[:3]
    p4_t = p4_t[:3]
    p5_t = p5_t[:3]
    p6_t = p6_t[:3]
    p7_t = p7_t[:3]
    p8_t = p8_t[:3]

    return [p1_t,p2_t, p3_t, p4_t, p5_t, p6_t, p7_t, p8_t]


#HASTA AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII    
# Set the view 
setaxis(-15,15,-15,15,-15,15)

# plot the axis
fix_system(10,1)

p1_init = [0,0,0]
p2_init = [7,0,0]
p3_init = [7,0,3]
p4_init = [0,0,3]
p5_init = [0,2,0]
p6_init = [7,2,0]
p7_init = [7,2,3]
p8_init = [0,2,3]


drawBox(p1_init, p2_init, p3_init, p4_init,
        p5_init, p6_init, p7_init, p8_init)


box_moved = move_Box(p1_init, p2_init, p3_init, p4_init, p5_init, p6_init, p7_init, p8_init, 4, 4, 4)


drawBox(box_moved[0],box_moved[1],box_moved[2],box_moved[3],box_moved[4],box_moved[5],box_moved[6],box_moved[7])



# show image.
plt.draw()
plt.show()
