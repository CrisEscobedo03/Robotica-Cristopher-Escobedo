# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# activar modo interactivo
plt.ion()

# create the fig and ax objects to handle figure and axes of the fixed frame
fig, ax = plt.subplots()
ax = plt.axes(projection="3d")


def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)
    ax.set_ylim3d(y1, y2)
    ax.set_zlim3d(z1, z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color="red", linewidth=linewidth)
    ax.plot3D(zp, y, zp, color="green", linewidth=linewidth)
    ax.plot3D(zp, zp, z, color="blue", linewidth=linewidth)


def sind(t):
    return np.sin(t * np.pi / 180)


def cosd(t):
    return np.cos(t * np.pi / 180)


def TRx(t):
    return np.array([[1, 0, 0, 0],
                     [0, cosd(t), -sind(t), 0],
                     [0, sind(t), cosd(t), 0],
                     [0, 0, 0, 1]])


def TRy(t):
    return np.array([[cosd(t), 0, sind(t), 0],
                     [0, 1, 0, 0],
                     [-sind(t), 0, cosd(t), 0],
                     [0, 0, 0, 1]])


def TRz(t):
    return np.array([[cosd(t), -sind(t), 0, 0],
                     [sind(t), cosd(t), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def TTx(t):
    return np.array([[1, 0, 0, t],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def TTy(t):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, t],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])


def TTz(t):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, t],
                     [0, 0, 0, 1]])


def drawVector(p_fin, p_init=[0, 0, 0], color="black", linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ, color=color, linewidth=linewidth)


def drawMobileFrame(origin, x, y, z):
    x = [(origin[0] + x[0]), (origin[1] + x[1]), (origin[2] + x[2])]
    y = [(origin[0] + y[0]), (origin[1] + y[1]), (origin[2] + y[2])]
    z = [(origin[0] + z[0]), (origin[1] + z[1]), (origin[2] + z[2])]

    drawVector(x, origin, color="red")
    drawVector(y, origin, color="green")
    drawVector(z, origin, color="blue")


def getUnitaryVectorsFromMatrix(TM):
    x = [TM[0][0], TM[1][0], TM[2][0]]
    y = [TM[0][1], TM[1][1], TM[2][1]]
    z = [TM[0][2], TM[1][2], TM[2][2]]
    origin = [TM[0][3], TM[1][3], TM[2][3]]
    return [x, y, z, origin]


# parámetros
l1 = 15
l2 = 5
l3 = 7
theta1 = 30

# ==============================
# 1) ANIMACIÓN EN Z (robot moviéndose)
# ==============================
n = 0
while n <= theta1:
    ax.cla()
    setaxis(-20, 20, -20, 20, -20, 20)
    fix_system(10, linewidth=1)

    T1 = TRz(n)
    [x1, y1, z1, origin1] = getUnitaryVectorsFromMatrix(T1)
    drawMobileFrame(origin1, x1, y1, z1)

    T12 = T1.dot(TTx(l1))
    [x2, y2, z2, origin2] = getUnitaryVectorsFromMatrix(T12)
    drawMobileFrame(origin2, x2, y2, z2)

    T123 = T12.dot(TRz(n))
    [x3, y3, z3, origin3] = getUnitaryVectorsFromMatrix(T123)
    drawMobileFrame(origin3, x3, y3, z3)

    T1234 = T123.dot(TTx(l2))
    [x4, y4, z4, origin4] = getUnitaryVectorsFromMatrix(T1234)
    drawMobileFrame(origin4, x4, y4, z4)

    T12345 = T1234.dot(TRz(n))
    [x5, y5, z5, origin5] = getUnitaryVectorsFromMatrix(T12345)
    drawMobileFrame(origin5, x5, y5, z5)

    T123456 = T12345.dot(TTx(l3))
    [x6, y6, z6, origin6] = getUnitaryVectorsFromMatrix(T123456)
    drawMobileFrame(origin6, x6, y6, z6)

    # ---- Dibujar los brazos
    drawVector(origin2, origin1, color="black", linewidth=4)
    drawVector(origin4, origin3, color="black", linewidth=4)
    drawVector(origin6, origin5, color="black", linewidth=4)

    n += 1
    plt.draw()
    plt.pause(0.01)

# ==============================
# 2) ROTACIÓN FINAL EN Y (mueve todo el robot)
# ==============================
m = 0
while m <= theta1:
    ax.cla()
    setaxis(-20, 20, -20, 20, -20, 20)
    fix_system(10, linewidth=1)

    # aplicar la rotación en Y al robot completo
    Ty_final = TRx(m)

    # Base
    T1 = Ty_final.dot(TRz(theta1))
    [x1, y1, z1, origin1] = getUnitaryVectorsFromMatrix(T1)
    drawMobileFrame(origin1, x1, y1, z1)

    T12 = T1.dot(TTx(l1))
    [x2, y2, z2, origin2] = getUnitaryVectorsFromMatrix(T12)
    drawMobileFrame(origin2, x2, y2, z2)

    T123 = T12.dot(TRz(theta1))
    [x3, y3, z3, origin3] = getUnitaryVectorsFromMatrix(T123)
    drawMobileFrame(origin3, x3, y3, z3)

    T1234 = T123.dot(TTx(l2))
    [x4, y4, z4, origin4] = getUnitaryVectorsFromMatrix(T1234)
    drawMobileFrame(origin4, x4, y4, z4)

    T12345 = T1234.dot(TRz(theta1))
    [x5, y5, z5, origin5] = getUnitaryVectorsFromMatrix(T12345)
    drawMobileFrame(origin5, x5, y5, z5)

    T123456 = T12345.dot(TTx(l3))
    [x6, y6, z6, origin6] = getUnitaryVectorsFromMatrix(T123456)
    drawMobileFrame(origin6, x6, y6, z6)

    # ---- Dibujar los brazos
    drawVector(origin2, origin1, color="black", linewidth=4)
    drawVector(origin4, origin3, color="black", linewidth=4)
    drawVector(origin6, origin5, color="black", linewidth=4)

    m += 1
    plt.draw()
    plt.pause(0.01)

# apagar modo interactivo y mostrar
plt.ioff()
plt.show()
