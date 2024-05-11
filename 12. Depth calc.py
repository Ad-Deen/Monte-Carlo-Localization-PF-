import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
from matplotlib.animation import FuncAnimation

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
initial_orientation = 45  # Initial orientation in degrees

# Function to calculate distance readings in a given direction
def calculate_distances(robot_position, orientation, occupancy_grid):
    distances = []
    for angle in [-30, 0, 30]:
        angle_rad = np.deg2rad(orientation + angle)
        for r in range(1, max(grid_size)):
            x = int(robot_position[0] + r * np.cos(angle_rad))
            y = int(robot_position[1] + r * np.sin(angle_rad))
            if 0 <= x < grid_size[0] and 0 <= y < grid_size[1]:
                if occupancy_grid[x, y] == 1:
                    distances.append((r, (x, y)))
                    break
        else:
            distances.append((0, None))  # No obstacle found within FOV, assign 0 distance
    return distances

# Function to update the plot for each frame of animation
def update(frame):
    plt.clf()
    
    # Calculate new robot orientation
    robot_orientation1 = initial_orientation + 1 * frame    #arrow orientation
    robot_orientation2 = initial_orientation - 1 * frame    #distance orientation
    
    # Plot the occupancy grid
    plt.imshow(occupancy_grid, cmap='binary', origin='lower')

    # Plot the robot position
    plt.scatter(robot_position[1], robot_position[0], color='red', marker='o', label='Robot')

    # Plot arrow indicating robot orientation
    arrow_length = 1
    arrow_dx = arrow_length * np.cos(np.deg2rad(robot_orientation1))
    arrow_dy = arrow_length * np.sin(np.deg2rad(robot_orientation1))
    # plt.arrow(robot_position[1], robot_position[0], arrow_dx, arrow_dy, color='blue', width=0.05, label='Orientation')
    
    # Calculate distances and plot arrows and white dots
    distances = calculate_distances(robot_position, robot_orientation2, occupancy_grid)
    d1, d2, d3 = distances
    d1 = d1[0]
    d2 = d2[0]
    d3 = d3[0]

    print(distances)
    
    for angle, (distance, pos) in zip([-30, 0, 30], distances):
        if distance > 0:
            # Calculate arrow orientation
            arrow_orientation = robot_orientation1 + angle
            
            # Plot arrow
            arrow_dx = arrow_length * np.cos(np.deg2rad(arrow_orientation))
            arrow_dy = arrow_length * np.sin(np.deg2rad(arrow_orientation))
            plt.arrow(robot_position[1], robot_position[0], arrow_dx, arrow_dy, color='green', width=0.05, label='Direction')
            
            # Plot white dot
            plt.scatter(pos[1], pos[0], color='white', marker='o')

    # Plot settings
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Frame: {frame}, Distances: d1={d1}, d2={d2}, d3={d3}')
    # plt.legend()
    plt.grid(True)

# Create animation
fig = plt.figure()
animation = FuncAnimation(fig, update, frames=range(500), interval=100)
plt.show()
