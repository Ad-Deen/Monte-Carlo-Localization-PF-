import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the size of the occupancy grid
grid_size = (20, 20)

# Create an empty occupancy grid
occupancy_grid = np.zeros(grid_size)

converge_spread = 0.8

# Add boundary obstacles
occupancy_grid[0, :] = 1
occupancy_grid[-1, :] = 1
occupancy_grid[:, 0] = 1
occupancy_grid[:, -1] = 1

# Add some obstacles inside the bounding box
occupancy_grid[5:8, 5:8] = 1
occupancy_grid[12:15, 10:13] = 1

# Define robot position
robot_position = (1, 18)
initial_orientation = 45  # Initial orientation in degrees
robot_orientation_change = 5  # Rotation change per frame for the robot
particle_orientation_change = 5  # Rotation change per frame for particles

def generate_mean_particles(occupancy_grid, particle_coordinates, num_particles):
    # Calculate the mean position of all existing particles
    mean_x = np.mean([coord[0] for coord in particle_coordinates])
    mean_y = np.mean([coord[1] for coord in particle_coordinates])
    print([mean_x,mean_y])
    # Initialize a list to store new particle coordinates
    new_particles = []
    
    # Iterate over possible positions in the occupancy grid
    for i in range(occupancy_grid.shape[0]):
        for j in range(occupancy_grid.shape[1]):
            # Check if the position is free and within a 2-unit radius of the mean position
            if occupancy_grid[i, j] == 0 and np.sqrt((i - mean_x) ** 2 + (j - mean_y) ** 2) <= 2:
                new_particles.append((i, j))
    
    # Randomly select num_particles from the available new particles
    if len(new_particles) > num_particles:
        random_indices = np.random.choice(len(new_particles), size=num_particles, replace=False)
        new_particles = [new_particles[i] for i in random_indices]
    
    return new_particles
'''Gives a bell curve on a given orientation list'''
def generate_normal_orientations(orientations, num_orientations, spread_factor=10):
    # Calculate the mean of the input orientations
    mean_orientation = np.mean(orientations)
    print(mean_orientation)
    # Generate normally distributed orientations around the mean
    normal_orientations = np.random.normal(mean_orientation, spread_factor, num_orientations)
    
    return normal_orientations.tolist()



# Function to generate random particles in free space
def generate_random_particles(occupancy_grid, num_particles):
    free_spaces = np.argwhere(occupancy_grid == 0)  # Find free spaces in the grid
    random_indices = np.random.choice(len(free_spaces), size=num_particles, replace=False)  # Randomly select indices
    particles = free_spaces[random_indices]  # Get particle positions from free spaces
    return particles

# Function to calculate distance to obstacle from a given position along a specified orientation
def calculate_distance_to_obstacle(position, orientation):
    x, y = position
    angle_rad = np.deg2rad(orientation)
    for r in range(1, max(grid_size)):
        x_pos = int(x + r * np.cos(angle_rad))
        y_pos = int(y + r * np.sin(angle_rad))
        if 0 <= x_pos < grid_size[0] and 0 <= y_pos < grid_size[1]:
            if occupancy_grid[x_pos, y_pos] == 1:
                return r
    return None

# Generate random particles
num_particles = 100
particles = generate_random_particles(occupancy_grid, num_particles)
# print(particles[0])
# Assign random main axis to particles
particle_orientations = np.random.uniform(0, 360, size=num_particles)
# print(particle_orientations)

# Lists to store particles and orientations after filtering
new_particles = []
new_orientations = []

# Function to update the plot for each frame of animation
def update(frame):
    global particles, particle_orientations , new_orientations, new_particles  # Move global declarations here
    
    plt.clf()
    
    # Update robot orientation
    global initial_orientation
    initial_orientation += robot_orientation_change

    # Plot the occupancy grid
    plt.imshow(occupancy_grid, cmap='binary', origin='lower')

    # Plot the robot position
    plt.scatter(robot_position[1], robot_position[0], color='red', marker='o', label='Robot')

    # Plot arrow indicating robot orientation
    arrow_length = 1
    arrow_dx = arrow_length * np.cos(np.deg2rad(initial_orientation))
    arrow_dy = arrow_length * np.sin(np.deg2rad(initial_orientation))
    plt.arrow(robot_position[1], robot_position[0], arrow_dx, arrow_dy, color='blue', width=0.1, label='Orientation')

    

    # Rotate particles according to their main axis and filter based on distance error
    for particle, particle_orientation in zip(particles, particle_orientations):
        x, y = particle
        # Update orientation
        particle_orientation -= particle_orientation_change
        # Calculate distance to obstacle along main axis direction
        distance_to_obstacle_particle = calculate_distance_to_obstacle((x, y), particle_orientation)
        # Calculate distance to obstacle along robot's main axis direction
        distance_to_obstacle_robot = calculate_distance_to_obstacle(robot_position, initial_orientation)
        # Calculate error
        if distance_to_obstacle_robot is not None and distance_to_obstacle_particle is not None:
            error = abs(distance_to_obstacle_particle - distance_to_obstacle_robot) / distance_to_obstacle_robot
        else:
            error = 1  # Assign maximum error if distance cannot be measured
        # Keep particles with error less than 50%
        if error <= 0.5:
            new_particles.append(particle)              #[x,y] coordinates of each particla retained after the filter
            # new_particles.append([particle[0] , particle[1]+1])
            # new_particles.append([particle[0]-1 , particle[1]+.25])
            # new_particles.append([particle[0]+1 , particle[1]+.25])
            # new_particles.append([particle[0]-0.5 , particle[1]-0.75])
            # new_particles.append([particle[0]+0.5 , particle[1]-0.75])

            new_orientations.append(particle_orientation)   # orientations in degrees
            # new_orientations.append(particle_orientation)
            # new_orientations.append(particle_orientation)
            # new_orientations.append(particle_orientation)
            # new_orientations.append(particle_orientation)
            # new_orientations.append(particle_orientation)

            # print(particle_orientation)
            # Plot main axis arrow
            main_axis_length = 0.5
            main_axis_dx = main_axis_length * np.cos(np.deg2rad(particle_orientation))
            main_axis_dy = main_axis_length * np.sin(np.deg2rad(particle_orientation))
            plt.arrow(y, x, main_axis_dy, main_axis_dx, color='green', width=0.05)
            # Plot point on particle position
            plt.scatter(y, x, color='black', marker='o')

    # Update particles and orientations
    more = 100 - len(new_particles)
    regen = list(generate_mean_particles(occupancy_grid, new_particles , int(more*converge_spread))) + list(generate_random_particles(occupancy_grid,int(more*(1-converge_spread))))
    regen_or = list(np.random.uniform(0, 360, size=int(more*(1-converge_spread)))) + generate_normal_orientations(new_orientations, int(more*converge_spread),spread_factor=30)
    # print(f" added point no.{len(regen)}")
    
    # print(f"needed = {more}")

    particles = np.array(new_particles + regen)
    particle_orientations = np.array(new_orientations + regen_or)

    # Plot settings
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Frame: {frame}')
    plt.grid(True)

# Create animation
fig = plt.figure()
animation = FuncAnimation(fig, update, frames=range(400), interval=100)
plt.show()
