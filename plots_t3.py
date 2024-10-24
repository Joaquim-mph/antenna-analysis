import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load the original CSV data
file_path = 'S11_vdipole.csv'  # Replace with your first CSV file path
data = pd.read_csv(file_path, delimiter=';', decimal='.')
data['Frequency'] = pd.to_numeric(data['Frequency']) / 1e6  # Convert to MHz

# Load the second CSV data
new_file_path = 'S11_simulation.csv'  # Replace with your second CSV file path
new_data = pd.read_csv(new_file_path, delimiter=',')

# Plot both datasets on the same figure
plt.figure(figsize=(7, 5))

# Plot the original data (S11-Gain)
plt.plot(data['Frequency'], data['S11-Gain (dB)'], marker='x', linestyle='--', label='S11 medido')

# Plot the new data (S(1,1) - dB values)
plt.plot(new_data['Freq [MHz]'], new_data['dB(S(1,1)) []'], color='green', label='S11 simulación HFSS')

# Add labels and title
plt.xlabel('Frequency (MHz)')
plt.ylabel('S11 (dB)')
plt.grid(True)
plt.legend()

# Display the first plot
plt.show()

# Now for the 3D radiation pattern plot in spherical coordinates
# Load the radiation pattern data from your CSV
radiation_file_path = 'radiation_pattern.csv'  # Replace with your actual radiation pattern CSV file path
radiation_data = pd.read_csv(radiation_file_path)

# Convert degrees to radians for Phi and Theta
radiation_data['Phi[rad]'] = np.radians(radiation_data['Phi[deg]'])
radiation_data['Theta[rad]'] = np.radians(radiation_data['Theta[deg]'])

# Convert the gain (r) values from dB to linear scale for better visualization in 3D space
# This step is optional depending on how you want the gain to be represented
gain = 10 ** (radiation_data['dB10normalize(GainTotal)'] / 10.0)

# Convert spherical coordinates (Phi, Theta, Gain) to Cartesian coordinates (x, y, z)
x = gain * np.sin(radiation_data['Theta[rad]']) * np.cos(radiation_data['Phi[rad]'])
y = gain * np.sin(radiation_data['Theta[rad]']) * np.sin(radiation_data['Phi[rad]'])
z = gain * np.cos(radiation_data['Theta[rad]'])

# Prepare the figure for the 3D radiation pattern plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D radiation pattern using scatter plot
sc = ax.scatter(x, y, z, c=gain, cmap='viridis')

# Add color bar for reference
plt.colorbar(sc, ax=ax)

# Label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display the second plot (3D radiation pattern in Cartesian coordinates)
plt.show()
