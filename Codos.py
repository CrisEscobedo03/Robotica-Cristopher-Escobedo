import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------ CINEMÁTICA INVERSA ------------------

def ik_2r(L1, L2, x, y, elbow='up'):

    r2 = x**2 + y**2
    L_sum = L1 + L2
    L_diff = abs(L1 - L2)
    
    if r2 > L_sum**2 or r2 < L_diff**2:
        return None  # fuera de alcance

    # Ley de cosenos
    cos_theta2 = (r2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1, 1)
    theta2 = np.arccos(cos_theta2)
    
    if elbow == 'down':
        theta2 = -theta2

    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return np.degrees(theta1), np.degrees(theta2)

# ------------------ CINEMÁTICA DIRECTA ------------------

def fk_2r(L1, L2, theta1_deg, theta2_deg):
  
    t1 = np.radians(theta1_deg)
    t2 = np.radians(theta2_deg)
    x0, y0 = 0, 0
    x1, y1 = L1 * np.cos(t1), L1 * np.sin(t1)
    x2, y2 = x1 + L2 * np.cos(t1 + t2), y1 + L2 * np.sin(t1 + t2)
    return np.array([x0, x1, x2]), np.array([y0, y1, y2])

# ------------------ ANIMACIÓN ------------------

def animate_arm(L1, L2, x_target, y_target, elbow='up', steps=100):
    ik_result = ik_2r(L1, L2, x_target, y_target, elbow)
    if ik_result is None:
        print("Objetivo fuera del alcance")
        return
    
    theta1_end, theta2_end = ik_result

    # Trayectoria lineal del efector
    x_traj = np.linspace(L1 + L2, x_target, steps)
    y_traj = np.linspace(0, y_target, steps)

    # Guardar ángulos para cada paso
    theta1_vals = []
    theta2_vals = []

    for x, y in zip(x_traj, y_traj):
        res = ik_2r(L1, L2, x, y, elbow)
        if res is None:
            print(f"Punto ({x:.2f},{y:.2f}) fuera del alcance")
            return
        theta1_vals.append(res[0])
        theta2_vals.append(res[1])

    # Configurar figura
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-L1-L2-1, L1+L2+1)
    ax.set_ylim(-L1-L2-1, L1+L2+1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

    line, = ax.plot([], [], [], 'o-', lw=3, markersize=8, color='blue')
    target_dot = ax.scatter([x_target], [y_target], [0], marker='x', s=100, c='red')

    def update(i):
        xs, ys = fk_2r(L1, L2, theta1_vals[i], theta2_vals[i])
        zs = [0,0,0]
        line.set_data(xs, ys)
        line.set_3d_properties(zs)
        return line,

    anim = FuncAnimation(fig, update, frames=steps, interval=30, blit=False)
    plt.show()

# ------------------ LOOP INTERACTIVO ------------------

def main():
    print("=== Robot 2R Planar - Animación ===")
    while True:
        try:
            elbow = input("Modo (up/down) [up]: ").strip().lower()
            if elbow == 'q': break
            if elbow not in ['up','down','']:
                elbow = 'up'
            elif elbow == '':
                elbow = 'up'

            L1 = input("Longitud L1: ")
            if L1 == 'q': break
            L2 = input("Longitud L2: ")
            if L2 == 'q': break
            x = input("Coordenada X objetivo: ")
            if x == 'q': break
            y = input("Coordenada Y objetivo: ")
            if y == 'q': break

            L1, L2, x, y = float(L1), float(L2), float(x), float(y)

            animate_arm(L1, L2, x, y, elbow)
        except KeyboardInterrupt:
            print("\nSaliendo...")
            break
        except Exception as e:
            print(f"[ERROR] {e}")
            continue

if __name__ == "__main__":
    main()
