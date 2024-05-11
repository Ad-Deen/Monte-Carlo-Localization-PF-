import numpy as np
import matplotlib.pyplot as plt

# Size of the grid
grid_size = 10

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


# Function to update the animation
def update(frame):
    global particles, robot_pose
    
    k = ((1+frame)/500)*55
    # Simulate robot movement
    movement = [0.15, 0, np.pi/k]  # Example movement: distance, no sideways movement, rotation
    # Update actual robot pose based on movement
    robot_pose[0] += movement[0] * np.cos(robot_pose[2])  # Update x-coordinate
    robot_pose[1] += movement[0] * np.sin(robot_pose[2])  # Update y-coordinate
    robot_pose[2] += movement[2]  # Update orientation (theta)

    # Update particles based on motion
    particles = motion_model(particles, movement)
    
    # Count the number of remaining pose estimations after removing particles that collide with the boundary
    remaining_poses = np.sum((particles[:, 0] >= 1) & (particles[:, 0] <= grid_size - 2) &
                             (particles[:, 1] >= 1) & (particles[:, 1] <= grid_size - 2))

    # Calculate the estimated pose (average position of remaining particles)
    if remaining_poses > 0:
        filtered_particles = particles[(particles[:, 0] >= 1) & (particles[:, 0] <= grid_size - 2) &
                                       (particles[:, 1] >= 1) & (particles[:, 1] <= grid_size - 2)]
        estimated_pose = np.mean(filtered_particles, axis=0)
    else:
        estimated_pose = robot_pose  # If all particles collide with the boundary, use actual pose

    # Clear the previous plot
    plt.clf()

    # Visualize the grid, particles, and robot pose using Matplotlib
    plt.xlim(0, grid_size - 1)
    plt.ylim(0, grid_size - 1)
    plt.scatter(particles[:, 0], particles[:, 1], color='blue', alpha=0.5, label='Particles')
    plt.scatter(robot_pose[0], robot_pose[1], color='red', label='Actual Robot Pose', s=100)
    plt.scatter(estimated_pose[0], estimated_pose[1], color='green', label='Estimated Robot Pose')
    plt.legend()
    plt.title(f"Iteration {frame + 1} - Remaining Pose Estimations: {remaining_poses}")  # Add title with iteration number and remaining pose estimations

# Create animation
num_iterations = 500
for i in range(num_iterations):
    update(i)
    plt.pause(0.1)  # Pause to visualize each iteration

# Show the final plot
plt.show()
