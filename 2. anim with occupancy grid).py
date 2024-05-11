import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Size of the grid
grid_size = 10

# Create occupancy grid
occupancy_grid = np.zeros((grid_size, grid_size))

# Define borders as obstacles
occupancy_grid[0, :] = 1  # Top border
occupancy_grid[-1, :] = 1  # Bottom border
occupancy_grid[:, 0] = 1  # Left border
occupancy_grid[:, -1] = 1  # Right border

# Robot pose (initial position and orientation)
robot_pose = [5, 5, np.pi/2]  # Example: x, y, theta

# Number of particles
num_particles = 100

# Initial particle positions (randomly distributed around robot pose)
particles = np.column_stack((np.random.randint(1, grid_size-1, num_particles),
                             np.random.randint(1, grid_size-1, num_particles),
                             np.random.rand(num_particles) * 2 * np.pi))

def motion_model(particles, movement):
    # Update particle positions based on movement and noise
    new_particles = particles + movement
    # Prevent particles from moving outside the grid
    new_particles[:, 0] = np.clip(new_particles[:, 0], 1, grid_size - 2)
    new_particles[:, 1] = np.clip(new_particles[:, 1], 1, grid_size - 2)
    return new_particles

def sensor_model(particles, sensor_data):
    # Update particle weights based on sensor data and map
    weights = np.zeros(num_particles)
    for i, particle in enumerate(particles):
        # Check if the particle's position is an obstacle
        if occupancy_grid[int(particle[1]), int(particle[0])] == 1:
            # If the particle is at an obstacle, assign zero weight
            weights[i] = 0
        else:
            # Otherwise, assign a default weight of 1
            weights[i] = 1
    return weights

def resample_particles(particles, weights):
    # Check if all weights are zeros
    if np.all(weights == 0):
        # If all weights are zeros, assign equal weights to all particles
        weights = np.ones(len(weights)) / len(weights)
    else:
        # Normalize weights
        weights /= np.sum(weights)
    
    # Resample particles based on their weights
    # Higher weight -> more likely to be replicated
    indices = np.random.choice(np.arange(len(particles)), size=num_particles, p=weights)
    return particles[indices]

# Function to update the animation
def update(frame):
    global particles

    # Simulate robot movement and sensor data acquisition
    movement = [0.5, 0.5, np.pi/6]  # Example movement: distance, sideways movement, rotation
    sensor_data = [np.pi/2]  # Example sensor data: robot orientation (replace with actual sensor data)

    # Update particles based on motion
    particles = motion_model(particles, movement)

    # Update weights based on sensor model
    weights = sensor_model(particles, sensor_data)

    # Resample particles for better localization estimate
    particles = resample_particles(particles, weights)

    # Extract estimated robot pose from particles (e.g., average or highest weight)
    estimated_pose = np.average(particles, axis=0)

    # Clear the previous plot
    plt.clf()

    # Visualize the occupancy grid, particles, and estimated robot pose using Matplotlib
    plt.imshow(occupancy_grid, cmap='binary', origin="lower")
    plt.scatter(particles[:, 0], particles[:, 1], alpha=0.4)
    plt.plot(estimated_pose[0], estimated_pose[1], marker='o', color='red', label='Estimated Pose')
    plt.legend()
    plt.title(f"Iteration {frame + 1}")  # Add title with iteration number

# Create animation
ani = FuncAnimation(plt.gcf(), update, frames=30, interval=500)  # 10 frames, 500 milliseconds interval between frames

# Show the animation
plt.show()
