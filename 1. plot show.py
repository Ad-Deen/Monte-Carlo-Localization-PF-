import numpy as np
import matplotlib.pyplot as plt

# Environment map (replace with your map representation)
environment_map = np.zeros((10, 10))  # Create a 10x10 map

# Robot pose (initial position and orientation)
robot_pose = [5, 5, np.pi/2]  # Example: x, y, theta

# Number of particles
num_particles = 100

# Initial particle positions (randomly distributed around robot pose)
particles = robot_pose + np.random.rand(num_particles, 3)

def motion_model(particles, movement):
    # Update particle positions based on movement and noise
    particles[:, 0:2] += movement[0:2] + np.random.randn(num_particles, 2)
    particles[:, 2] += movement[2] + np.random.randn(num_particles) * 0.1  # Add noise to orientation
    return particles

def sensor_model(particles, sensor_data):
    # Update particle weights based on sensor data and map
    weights = np.zeros(num_particles)
    for i, particle in enumerate(particles):
        # Calculate the angle between the particle orientation and the sensor direction
        angle_diff = np.abs(particle[2] - sensor_data[0])
        if angle_diff <= np.deg2rad(50):  # Assuming sensor FOV is +/- 50 degrees
            # If the particle is within the sensor FOV, increase its weight
            weights[i] = 1.0
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

# Main loop (simulation)
for iteration in range(10):
    # Simulate robot movement and sensor data acquisition
    movement = [1, 0.5, np.pi/6]  # Example movement: distance, sideways movement, rotation
    sensor_data = [np.pi/2]  # Example sensor data: robot orientation (replace with actual sensor data)

    # Update particles based on motion
    particles = motion_model(particles, movement)

    # Update weights based on sensor model
    weights = sensor_model(particles, sensor_data)

    # Resample particles for better localization estimate
    particles = resample_particles(particles, weights)

    # Extract estimated robot pose from particles (e.g., average or highest weight)
    estimated_pose = np.average(particles, axis=0)

    # Visualize the environment, particles, and estimated robot pose using Matplotlib
    plt.figure()  # Create a new figure for each iteration
    plt.imshow(environment_map, origin="lower")
    plt.scatter(particles[:, 0], particles[:, 1], alpha=0.4)
    plt.plot(estimated_pose[0], estimated_pose[1], marker='o', color='red', label='Estimated Pose')
    plt.legend()
    plt.title(f"Iteration {iteration + 1}")  # Add title with iteration number
    plt.pause(0.5)  # Pause for 0.5 seconds to see each iteration
    plt.close()  # Close the current plot window

plt.show()
