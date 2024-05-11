import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow

# Define the size of the occupancy grid
grid_size = (20, 20)

# Create an empty occupancy grid
occupancy_grid = np.zeros(grid_size)

# Add boundary obstacles
occupancy_grid[0, :] = 1
occupancy_grid[-1, :] = 1
occupancy_grid[:, 0] = 1
occupancy_grid[:, -1] = 1

# Add some obstacles inside the bounding box
occupancy_grid[5:8, 5:8] = 1
occupancy_grid[12:15, 10:13] = 1

# Define robot position
robot_position = (10, 10)
robot_orientation = 45  # Orientation in degrees

# Plot the occupancy grid
plt.imshow(occupancy_grid, cmap='binary', origin='lower')

# Plot the robot position
plt.scatter(robot_position[1], robot_position[0], color='red', marker='o', label='Robot')

# Plot arrow indicating robot orientation
arrow_length = 1
arrow_dx = arrow_length * np.cos(np.deg2rad(robot_orientation))
arrow_dy = arrow_length * np.sin(np.deg2rad(robot_orientation))
plt.arrow(robot_position[1], robot_position[0], arrow_dx, arrow_dy, color='blue', width=0.1, label='Orientation')

# Calculate distance to nearest obstacle in the direction of the arrow
angle_rad = np.deg2rad(robot_orientation)
for r in range(1, max(grid_size)):
    x = int(robot_position[0] + r * np.cos(angle_rad))
    y = int(robot_position[1] + r * np.sin(angle_rad))
    if 0 <= x < grid_size[0] and 0 <= y < grid_size[1]:
        if occupancy_grid[x, y] == 1:
            distance_to_obstacle = r
            plt.scatter(y, x, color='white', marker='o', label='Nearest Obstacle')
            break

# Plot settings
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Occupancy Grid with Robot, Orientation, and Nearest Obstacle')
plt.legend()
plt.grid(True)
plt.show()

print("Distance to nearest obstacle in the direction of the arrow:", distance_to_obstacle)
