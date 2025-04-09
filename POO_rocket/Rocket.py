import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

class Rocket:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.trajectory = [(self.x, self.y)]

    def move_up(self, step=1):
        self.y += step
        self._update_trajectory()

    def move_down(self, step=1):
        self.y -= step
        self._update_trajectory()

    def move_left(self, step=1):
        self.x -= step
        self._update_trajectory()

    def move_right(self, step=1):
        self.x += step
        self._update_trajectory()

    def clear(self):
        self.x = 0
        self.y = 0
        self.trajectory = [(self.x, self.y)]

    def _update_trajectory(self):
        self.trajectory.append((self.x, self.y))


class RocketApp:
    def __init__(self, root,x,y):
        self.root = root
        self.root.title("Rocket Trajectory Simulator")

        # Create Rocket
        self.rocket = Rocket(x,y)

        # Main frames
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)

        self.plot_frame = tk.Frame(main_frame)
        self.plot_frame.pack(side='left', padx=10, pady=10)

        self.control_frame = tk.Frame(main_frame)
        self.control_frame.pack(side='right', padx=10, pady=10)

        # Create figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack()

        # Create controller buttons with layout like ipywidgets style
        self._create_controller()

        # Label to display position
        self.position_label = tk.Label(self.control_frame, text=f"Position: ({self.rocket.x}, {self.rocket.y})")
        self.position_label.pack(pady=10)

        # Initial display
        self.update_display()

    def _create_controller(self):
        pad = {'padx': 5, 'pady': 5}

        row1 = tk.Frame(self.control_frame)
        row1.pack()
        tk.Label(row1, text=" ").pack(side='left', **pad)
        tk.Button(row1, text="↑", command=self.move_up, width=5).pack(side='left', **pad)
        tk.Label(row1, text=" ").pack(side='left', **pad)

        row2 = tk.Frame(self.control_frame)
        row2.pack()
        tk.Button(row2, text="←", command=self.move_left, width=5).pack(side='left', **pad)
        tk.Button(row2, text="Clear", command=self.clear, width=5).pack(side='left', **pad)
        tk.Button(row2, text="→", command=self.move_right, width=5).pack(side='left', **pad)

        row3 = tk.Frame(self.control_frame)
        row3.pack()
        tk.Label(row3, text=" ").pack(side='left', **pad)
        tk.Button(row3, text="↓", command=self.move_down, width=5).pack(side='left', **pad)
        tk.Label(row3, text=" ").pack(side='left', **pad)

    def update_display(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_xticks(np.arange(-10, 11, 1))
        self.ax.set_yticks(np.arange(-10, 11, 1))
        self.ax.grid(True, linestyle='--', alpha=0.7)

        if len(self.rocket.trajectory) >= 1:
            x, y = zip(*self.rocket.trajectory)
            self.ax.plot(x, y, 'ob-', alpha=0.5)
        self.ax.plot(self.rocket.x, self.rocket.y, 'ro', markersize=10)
        self.ax.set_title("Rocket Trajectory")
        self.canvas.draw()

        self.position_label.config(text=f"Position: ({self.rocket.x}, {self.rocket.y})")

    # Movement functions
    def move_up(self):
        self.rocket.move_up()
        self.update_display()

    def move_down(self):
        self.rocket.move_down()
        self.update_display()

    def move_left(self):
        self.rocket.move_left()
        self.update_display()

    def move_right(self):
        self.rocket.move_right()
        self.update_display()

    def clear(self):
        self.rocket.clear()
        self.update_display()


def run_app(x, y):
    root = tk.Tk()
    app = RocketApp(root, x, y)
    root.mainloop()

if __name__ == '__main__':
    from multiprocessing import Process

    p1 = Process(target=run_app, args=(5, 5))
    p2 = Process(target=run_app, args=(-5, -5))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
