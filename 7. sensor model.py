import numpy as np
import matplotlib.pyplot as plt

# Size of the grid
grid_size = 10

# Robot pose (initial position and orientation)
robot_pose = [5, 5, np.pi/2]  # Example: x, y, theta

# Number of particles
num_particles = 400

# Environment map (replace with your map representation)
environment_map = np.zeros((grid_size, grid_size))  # Create a grid map

# Initialize particles uniformly
particles_x = np.linspace(1, grid_size - 2, int(np.sqrt(num_particles)))
particles_y = np.linspace(1, grid_size - 2, int(np.sqrt(num_particles)))
particles_xx, particles_yy = np.meshgrid(particles_x, particles_y)
particles = np.column_stack((particles_xx.ravel(), particles_yy.ravel(), np.random.rand(num_particles) * 2 * np.pi))

def motion_model(particles, movement):
    # Update particle positions based on movement and noise
    for i in range(len(particles)):
        # Update orientation (theta) by adding the rotation component
        particles[i, 2] += movement[2]
        # Calculate the new position using polar coordinates
        new_x = particles[i, 0] + movement[0] * np.cos(particles[i, 2])  # Update x-coordinate
        new_y = particles[i, 1] + movement[0] * np.sin(particles[i, 2])  # Update y-coordinate
        # Check if the new position is within the map boundaries
        if 1 <= new_x <= grid_size - 2 and 1 <= new_y <= grid_size - 2:
            particles[i, 0] = new_x
            particles[i, 1] = new_y
        else:
            # If the new position is outside the map boundaries, remove the particle
            particles[i] = np.nan
    # Remove particles that are marked as nan
    particles = particles[~np.isnan(particles).any(axis=1)]
    return particles

def sensor_model(particles, sensor_data):
    # Update particle weights based on sensor data
    weights = np.zeros(len(particles))
    for i, particle in enumerate(particles):
        # Calculate distance from particle to sensor data (e.g., Euclidean distance)
        distance = np.sqrt((particle[0] - sensor_data[0])**2 + (particle[1] - sensor_data[1])**2)
        # Assign weight inversely proportional to distance
        weights[i] = 1.0 / (distance + 1e-10)  # Add a small value to avoid division by zero
    # Normalize weights
    weights /= np.sum(weights)
    return weights

# Main loop (simulation)
for _ in range(30):
    # Simulate robot movement and sensor data acquisition
    movement = [0.15, 0, np.pi/20]  # Example movement: distance, no sideways movement, rotation
    sensor_data = [robot_pose[0], robot_pose[1]]  # Example sensor data (replace with actual sensor data)

    # Update particles based on motion
    particles = motion_model(particles, movement)

    # Update weights based on sensor model
    weights = sensor_model(particles, sensor_data)

    # Resample particles for better localization estimate
    particles = particles[np.random.choice(len(particles), size=num_particles, p=weights)]

    # Extract estimated robot pose from particles (e.g., average or highest weight)
    estimated_pose = np.mean(particles, axis=0)

    # Visualize the environment, particles, and estimated robot pose using Matplotlib
    plt.cla()  # Clear previous plot
    plt.imshow(environment_map, origin="lower")
    plt.scatter(particles[:, 0], particles[:, 1], alpha=0.4)
    plt.plot(estimated_pose[0], estimated_pose[1], marker='o', color='red', label='Estimated Pose')
    plt.scatter(robot_pose[0], robot_pose[1], color='blue', label='Actual Pose')  # Show actual robot pose
    plt.legend()
    plt.title(f"Iteration {_ + 1}")  # Add title with iteration number
    plt.pause(0.2)  # Update plot animation

plt.show()
