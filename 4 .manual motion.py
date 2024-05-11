import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CarSimulation:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.occupancy_grid = np.zeros((grid_size, grid_size))
        self.car_pos = [grid_size // 2, grid_size // 2]
        self.car_angle = 0  # In radians
        self.car_size = 1
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, grid_size)
        self.ax.set_ylim(0, grid_size)
        self.car = patches.Rectangle((0, 0), self.car_size, 2*self.car_size, edgecolor='blue', facecolor='none')
        self.ax.add_patch(self.car)
        self.update_car_position()
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        plt.title("2D Car Simulation in Occupancy Grid")
        plt.grid(True)
        plt.show()

    def on_key(self, event):
        step_size = 1
        
        if event.key == 'up':
            self.car_pos[0] += step_size * np.cos(self.car_angle)
            self.car_pos[1] += step_size * np.sin(self.car_angle)
        elif event.key == 'down':
            self.car_pos[0] -= step_size * np.cos(self.car_angle)
            self.car_pos[1] -= step_size * np.sin(self.car_angle)
        elif event.key == 'left':
            self.car_angle += np.pi / 6  # Rotate left by 30 degrees
        elif event.key == 'right':
            self.car_angle -= np.pi / 6  # Rotate right by 30 degrees
        
        self.update_car_position()

    def update_car_position(self):
        self.car.set_xy((self.car_pos[0] - self.car_size / 2, self.car_pos[1] - self.car_size))
        self.car.angle = np.degrees(self.car_angle)  # Convert angle to degrees for rotation
        self.fig.canvas.draw()

if __name__ == "__main__":
    CarSimulation()
