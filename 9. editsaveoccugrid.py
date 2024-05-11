import numpy as np
import matplotlib.pyplot as plt

# Load the occupancy grid from the .npy file
environment_map = np.load('custom.npy')

# Define the start and end points of the line
start_point = (43, 11)  # Example start point (row, column)
end_point = (43, 4)    # Example end point (row, column)

def draw_horizontal_vertical_line(start, end, grid):
    # Extract coordinates
    x0, y0 = start
    x1, y1 = end
    
    # Ensure the line is either horizontal or vertical
    if x0 != x1 and y0 != y1:
        raise ValueError("Line must be horizontal or vertical")

    # Set the value of the line cells to 1 (occupied)
    if x0 == x1:  # Vertical line
        for y in range(min(y0, y1), max(y0, y1) + 1):
            grid[y, x0] = 0
    else:  # Horizontal line
        for x in range(min(x0, x1), max(x0, x1) + 1):
            grid[y0, x] = 0


# Draw the line on the occupancy grid
draw_horizontal_vertical_line(start_point, end_point, environment_map)


# Visualize the occupancy grid using Matplotlib
plt.imshow(environment_map, cmap='gray', origin='lower')
plt.title('Custom Occupancy Grid')  # Add a title
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()

# Save the modified occupancy grid with the same name
np.save('custom.npy', environment_map)
