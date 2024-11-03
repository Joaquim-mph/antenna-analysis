import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import scienceplots 

plt.style.use(['science','nature'])

# Load the CSV file (assuming it's in the same format as described)
file_path = 'radiation_pattern.csv'
data = pd.read_csv(file_path)

# Extracting the relevant columns
phi = np.radians(data['Phi[deg]'])
theta = np.radians(data['Theta[deg]'])
gain = data['dB10normalize(GainTotal)']

# Normalize gain values for coloring
gain_min = gain.min()
gain_max = gain.max()
norm_gain = (gain - gain_min) / (gain_max - gain_min)  # Normalize to range [0, 1]

# Convert spherical coordinates (phi, theta) to Cartesian coordinates for plotting
X = norm_gain*np.sin(theta) * np.cos(phi)
Y = norm_gain*np.sin(theta) * np.sin(phi)
Z = norm_gain*np.cos(theta)

# Plotting the 3D radiation pattern
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Create the plot with gain-based coloring
sc = ax.scatter(X, Y, Z, c=gain, cmap='jet', marker='o')

# Adding a color bar for the gain
cbar = plt.colorbar(sc, shrink=0.5, aspect=5)
cbar.set_label('Normalized Gain (dB)')

# Set plot titles and labels
#ax.set_title('3D Radiation Pattern')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set fixed axis limits from -1 to 1 for all axes
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

plt.show()


new_file_path = 'cross.csv'
new_data = pd.read_csv(new_file_path)


# Extract the columns from the new data
phi_cross = np.radians(new_data['Phi[deg]'])  # Convert to radians for the plot
gain_cross = new_data['dB10normalize(GainTotal)']

# Create a 2D polar plot to visualize the gain as a function of the azimuth angle (Phi)
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 6))

# Plot the gain as a function of Phi (Azimuth)
ax.plot(phi_cross, gain_cross, color='blue', label='Gain (dB)')

# Add labels and title
#ax.set_title('Cross-sectional Radiation Pattern (Theta = 90°)', va='bottom')
ax.set_theta_zero_location('N')  # Set zero degrees at the top
ax.set_theta_direction(-1)  # Plot clockwise

# Add a grid and legend
ax.grid(True)
ax.legend(loc='upper right')

# Show the plot
#plt.show()
