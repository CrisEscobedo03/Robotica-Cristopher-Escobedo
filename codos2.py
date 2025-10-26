import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------ CINEMÁTICA INVERSA YZ ------------------

def ik_2r_yz(L1, L2, y, z, elbow='up'):
 
    r2 = y**2 + z**2
    L_sum = L1 + L2
    L_diff = abs(L1 - L2)
    
    if r2 > L_sum**2 or r2 < L_diff**2:
        return None

    cos_theta2 = (r2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1, 1)
    theta2 = np.arccos(cos_theta2)
    
    if elbow == 'down':
        theta2 = -theta2

    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)
    theta1 = np.arctan2(z, y) - np.arctan2(k2, k1)

    return np.degrees(theta1), np.degrees(theta2)

# ------------------ CINEMÁTICA DIRECTA YZ ------------------

def fk_2r_yz(L1, L2, th1_deg, th2_deg):

    t1 = np.radians(th1_deg)
    t2 = np.radians(th2_deg)
    x0, y0, z0 = 0, 0, 0
    y1, z1 = L1*np.cos(t1), L1*np.sin(t1)
    y2, z2 = y1 + L2*np.cos(t1+t2), z1 + L2*np.sin(t1+t2)
    x1 = x2 = 0
    return np.array([x0, x1, x2]), np.array([y0, y1, y2]), np.array([z0, z1, z2])

# ------------------ ANIMACIÓN ------------------

def animate_arm_yz(L1, L2, y_target, z_target, elbow='up', steps=100):
    ik_result = ik_2r_yz(L1, L2, y_target, z_target, elbow)
    if ik_result is None:
        print("Objetivo fuera del alcance")
        return
    th1_end, th2_end = ik_result

    y_traj = np.linspace(L1+L2, y_target, steps)
    z_traj = np.linspace(0, z_target, steps)

    theta1_vals = []
    theta2_vals = []
    for y, z in zip(y_traj, z_traj):
        res = ik_2r_yz(L1, L2, y, z, elbow)
        if res is None:
            print(f"Punto ({y:.2f},{z:.2f}) fuera del alcance")
            return
        theta1_vals.append(res[0])
        theta2_vals.append(res[1])

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-L1-L2-1, L1+L2+1)
    ax.set_ylim(-L1-L2-1, L1+L2+1)
    ax.set_zlim(-L1-L2-1, L1+L2+1)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

    line, = ax.plot([], [], [], 'o-', lw=3, markersize=8, color='blue')
    target_dot = ax.scatter([0], [y_target], [z_target], marker='x', s=100, c='red')

    def update(i):
        xs, ys, zs = fk_2r_yz(L1, L2, theta1_vals[i], theta2_vals[i])
        line.set_data(xs, ys)
        line.set_3d_properties(zs)
        return line,

    anim = FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
    plt.show()

# ------------------ LOOP INTERACTIVO ------------------

def main():
    print("ROBOT 2D")
    while True:
        try:
            elbow = input("Modo (up/down) [up]: ").strip().lower()
            if elbow == 'q': break
            if elbow not in ['up','down','']: elbow = 'up'
            elif elbow == '': elbow = 'up'

            L1 = input("Longitud L1: ")
            if L1 == 'q': break
            L2 = input("Longitud L2: ")
            if L2 == 'q': break
            y = input("Coordenada Y objetivo: ")
            if y == 'q': break
            z = input("Coordenada Z objetivo: ")
            if z == 'q': break

            L1, L2, y, z = float(L1), float(L2), float(y), float(z)

            animate_arm_yz(L1, L2, y, z, elbow)
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

if __name__ == "__main__":
    main()
