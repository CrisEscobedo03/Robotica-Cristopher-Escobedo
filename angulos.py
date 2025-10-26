import numpy as np
import matplotlib.pyplot as plt

# Parámetros de simulación
MUNDO = 20
PASO = 1.5
PAUSA = 0.01

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# ------------------ Utilidades de dibujo ------------------

def dibujar_ejes():
    """Dibuja ejes fijos X (rojo), Y (azul), Z (verde)."""
    ax.plot([0,8],[0,0],[0,0], color='red', linewidth=1.5)
    ax.plot([0,0],[0,8],[0,0], color='blue', linewidth=1.5)
    ax.plot([0,0],[0,0],[0,8], color='green', linewidth=1.5)

def dibujar_vector(inicio, fin, color='black', lw=2.0):
    ax.plot([inicio[0], fin[0]],
            [inicio[1], fin[1]],
            [inicio[2], fin[2]], color=color, linewidth=lw)

def dibujar_frame(T, escala=2.0):
    o = T[:3,3]
    R = T[:3,:3]
    dibujar_vector(o, o+escala*R[:,0], 'red', 1.5)
    dibujar_vector(o, o+escala*R[:,1], 'blue', 1.5)
    dibujar_vector(o, o+escala*R[:,2], 'green',1.5)

def set_ejes(xmin, xmax, ymin, ymax, zmin, zmax):
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_zlim(zmin, zmax)
    ax.view_init(elev=30, azim=40)

def igual_aspecto():
    xl, yl, zl = np.array(ax.get_xlim3d()), np.array(ax.get_ylim3d()), np.array(ax.get_zlim3d())
    max_range = max((xl[1]-xl[0]), (yl[1]-yl[0]), (zl[1]-zl[0])) / 2
    cx, cy, cz = np.mean(xl), np.mean(yl), np.mean(zl)
    ax.set_xlim(cx-max_range, cx+max_range)
    ax.set_ylim(cy-max_range, cy+max_range)
    ax.set_zlim(cz-max_range, cz+max_range)

# ------------------ Cinemática ------------------

def Rx(t):
    c, s = np.cos(np.deg2rad(t)), np.sin(np.deg2rad(t))
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def A_DH(theta, d, a, alpha):
    ct, st = np.cos(np.deg2rad(theta)), np.sin(np.deg2rad(theta))
    ca, sa = np.cos(np.deg2rad(alpha)), np.sin(np.deg2rad(alpha))
    return np.array([
        [ct, -st*ca, st*sa, a*ct],
        [st, ct*ca, -ct*sa, a*st],
        [0, sa, ca, d],
        [0,0,0,1]
    ])

def construir_T(R=np.eye(3), t=(0,0,0)):
    T = np.eye(4)
    T[:3,:3] = R
    T[:3,3] = t
    return T

def frames_2R(theta1, theta2, l1, l2):
    A1 = A_DH(theta1,0,l1,0)
    A2 = A_DH(theta2,0,l2,0)
    G0 = np.eye(4)
    G1 = A1
    G2 = A1 @ A2
    return G0, G1, G2

def dibujar_brazo(frames):
    G0, G1, G2 = frames
    o0, o1, o2 = G0[:3,3], G1[:3,3], G2[:3,3]
    dibujar_vector(o0,o1,'black',4)
    dibujar_vector(o1,o2,'black',4)
    for G in (G0,G1,G2):
        dibujar_frame(G, 2.0)

# ------------------ Entrada usuario ------------------

def leer_flotante(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")

# ------------------ Animación ------------------

def animar_brazo(l1, l2, t1_obj, t2_obj):
    t1, t2 = 0.0, 0.0
    while t1 < t1_obj or t2 < t2_obj:
        t1 = min(t1+PASO, t1_obj)
        t2 = min(t2+PASO, t2_obj)
        ax.cla()
        set_ejes(-MUNDO, MUNDO, -MUNDO, MUNDO, -MUNDO, MUNDO)
        dibujar_ejes()
        frames = frames_2R(t1,t2,l1,l2)
        dibujar_brazo(frames)
        igual_aspecto()
        plt.pause(PASO)

# ------------------ Main ------------------

if __name__=="__main__":
    l1 = leer_flotante("Longitud l1: ")
    l2 = leer_flotante("Longitud l2: ")
    t1_obj = leer_flotante("Ángulo θ1 : ")
    t2_obj = leer_flotante("Ángulo θ2 : ")

    set_ejes(-MUNDO, MUNDO, -MUNDO, MUNDO, -MUNDO, MUNDO)
    dibujar_ejes()
    animar_brazo(l1, l2, t1_obj, t2_obj)
    plt.show()
