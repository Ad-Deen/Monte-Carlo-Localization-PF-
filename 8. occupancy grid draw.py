import numpy as np
import matplotlib.pyplot as plt

# Size of the grid
grid_size = 50

# Create a custom occupancy grid
environment_map = np.zeros((grid_size, grid_size))  # Initialize with ones (occupied)

# Set the inner region to zeros (free space)
environment_map[1:-1, 1:-1] = 1  # Exclude the boundary cells

# Function to handle mouse click events
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        # Convert mouse click coordinates to grid indices
        x_index = int(event.xdata + 0.5)
        y_index = int(event.ydata + 0.5)
        
        # Update the grid cell value to represent an obstacle or feature
        environment_map[y_index, x_index] = 0
        
        # Visualize the updated environment
        plt.imshow(environment_map, cmap='gray', origin='lower')
        plt.title('Custom Occupancy Grid')  # Add a title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.draw()  # Redraw the plot

# Function to handle plot window closing event
def onclose(event):
    # Save the numpy occupancy grid to a file in the local directory
    np.save('occupancy_grid.npy', environment_map)
    print("Occupancy grid saved as 'occupancy_grid.npy'.")

# Create a Matplotlib figure and connect the mouse click and plot window closing event handlers
fig, ax = plt.subplots()
cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
cid_close = fig.canvas.mpl_connect('close_event', onclose)

# Show the plot
plt.imshow(environment_map, cmap='gray', origin='lower')
plt.title('Custom Occupancy Grid')  # Add a title
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
