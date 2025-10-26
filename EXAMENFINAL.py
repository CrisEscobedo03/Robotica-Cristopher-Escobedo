import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ------------------ Robot SCARA ------------------
class SCARARobotAlt:
    def __init__(self, theta1_deg, L1, L2, base_h=776.0, platillo_r=100.0):
        self.theta1 = np.deg2rad(theta1_deg)
        self.L1 = L1
        self.L2 = L2
        self.base_h = base_h
        self.platillo_r = platillo_r

    def forward_kinematics(self, theta2_deg, piston_h, theta3_deg):
        th1, th2 = self.theta1, np.deg2rad(theta2_deg)

        # Puntos principales
        p_base = np.array([0,0,0])
        p_eje = np.array([0,0,self.base_h])
        p1 = np.array([self.L1*np.cos(th1), self.L1*np.sin(th1), self.base_h])
        p2 = np.array([p1[0] + self.L2*np.cos(th1+th2),
                       p1[1] + self.L2*np.sin(th1+th2),
                       self.base_h])  # brazo2 termina aquí en Z

        # Pistón: altura real
        p_top = np.array([p2[0], p2[1], piston_h])  # platillo sigue el pistón

        # Cuadrado del platillo
        angle = np.deg2rad(theta3_deg)
        corners = np.array([
            [-1, -1],
            [ 1, -1],
            [ 1,  1],
            [-1,  1]
        ]) * self.platillo_r

        # Rotar cuadrado
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle),  np.cos(angle)]])
        rotated = corners @ rot_matrix.T

        hx = p_top[0] + rotated[:,0]
        hy = p_top[1] + rotated[:,1]
        hz = np.full_like(hx, p_top[2])

        return p_base, p_eje, p1, p2, p_top, hx, hy, hz

# ------------------ Animación ------------------
class SCARASimulatorAlt:
    def __init__(self, robot, theta2_seq, piston_seq, theta3_seq):
        self.robot = robot
        self.theta2_seq = theta2_seq
        self.piston_seq = piston_seq
        self.theta3_seq = theta3_seq

        self.fig = plt.figure(figsize=(10,8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-2000, 2000)
        self.ax.set_ylim(-2000, 2000)
        self.ax.set_zlim(0, 2000)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.set_zlabel("Z axis")
        self.ax.set_title("EXAMEN — ROBOT SCARA")

        # Inicializar líneas
        self.lines = {
            'base_eje': self.ax.plot([],[],[],color='black', lw=4)[0],
            'brazo1': self.ax.plot([],[],[],color='purple', lw=6)[0],
            'brazo2': self.ax.plot([],[],[],color='cyan', lw=4)[0],
            'pist': self.ax.plot([],[],[],color='green', lw=4)[0]
        }

        # Crear platillo
        _, _, _, _, p_top, hx, hy, hz = self.robot.forward_kinematics(theta2_seq[0], piston_seq[0], theta3_seq[0])
        verts = [list(zip(hx, hy, hz))]
        self.platillo = Poly3DCollection(verts, facecolor='yellow', alpha=0.8)
        self.ax.add_collection3d(self.platillo)

        # Marcador superior
        self.top_marker = self.ax.scatter([p_top[0]], [p_top[1]], [p_top[2]], color='red', s=50)

    def update(self, i):
        p_base, p_eje, p1, p2, p_top, hx, hy, hz = self.robot.forward_kinematics(
            self.theta2_seq[i], self.piston_seq[i], self.theta3_seq[i]
        )

        # Actualizar líneas
        self.lines['base_eje'].set_data([p_base[0], p_eje[0]], [p_base[1], p_eje[1]])
        self.lines['base_eje'].set_3d_properties([p_base[2], p_eje[2]])

        self.lines['brazo1'].set_data([p_eje[0], p1[0]], [p_eje[1], p1[1]])
        self.lines['brazo1'].set_3d_properties([p_eje[2], p1[2]])

        self.lines['brazo2'].set_data([p1[0], p2[0]], [p1[1], p2[1]])
        self.lines['brazo2'].set_3d_properties([p1[2], p2[2]])

        self.lines['pist'].set_data([p2[0], p_top[0]], [p2[1], p_top[1]])
        self.lines['pist'].set_3d_properties([p2[2], p_top[2]])

        # Actualizar platillo
        verts = [list(zip(hx, hy, hz))]
        self.platillo.set_verts(verts)

        # Actualizar marcador superior
        self.top_marker._offsets3d = (np.array([p_top[0]]), np.array([p_top[1]]), np.array([p_top[2]]))

        return list(self.lines.values()) + [self.platillo, self.top_marker]

    def animate(self):
        ani = FuncAnimation(self.fig, self.update, frames=len(self.theta2_seq),
                            interval=40, blit=False, repeat=False)
        plt.show()

# ------------------ Main ------------------
if __name__ == "__main__":
    frames_brazo = 120 
    frames_piston = 120 
    frames_total = frames_brazo + frames_piston

    # Secuencia de theta2: mover de 0 a 90 en la primera fase, luego mantener
    theta2_seq = np.concatenate([
        np.linspace(0, 90, frames_brazo),
        np.full(frames_piston, 90)
    ])

    # Secuencia del pistón: mantener altura inicial durante la primera fase, luego bajar
    piston_seq = np.concatenate([
        np.full(frames_brazo, 880),
        np.linspace(880, 418.5, frames_piston)
    ])

    # Secuencia de rotación 
    theta3_seq = np.linspace(0, 360, frames_total)

    robot = SCARARobotAlt(theta1_deg=30, L1=715, L2=850)
    sim = SCARASimulatorAlt(robot, theta2_seq, piston_seq, theta3_seq)
    sim.animate()
