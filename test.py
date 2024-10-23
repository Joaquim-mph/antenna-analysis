import pandas as pd
import logging
from utils import *
import os
import numpy as np

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Define the paths to the CSV files
    file_path_measured = 'src/csv/pabloT4/S11_real_3G.csv'
    file_path_simulated = 'src/csv/pabloT4/S11_simulado_6GHz.csv'
    file_path_radiation = 'src/csv/pabloT4/pattern_2.csv'  # Radiation pattern file

    # Load the measured S11 data
    try:
        measured_data = load_s11_data(file_path_measured, delimiter=';', decimal='.', frequency_column='Frequency', s11_column='S11-Gain (dB)', frequency_factor=1e-9)
        logging.info("Measured data loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading measured data: {e}")
        return

    # Load the simulated S11 data
    try:
        simulated_data = load_s11_data(file_path_simulated, delimiter=',', decimal='.', frequency_column='Freq [GHz]', s11_column='dB(S(1,1)) []', frequency_factor=1)
        logging.info("Simulated data loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading simulated data: {e}")
        return


    # Create the dataset information for plotting
    measured_dataset_info = {
        'data': measured_data,
        'label': 'Measured S11',
        'frequency_column': 'Frequency',
        's11_column': 'S11-Gain (dB)',
        'marker': 'o',
        'linestyle': '-',
        'color': 'navy'
    }

    simulated_dataset_info = {
        'data': simulated_data,
        'label': 'Simulated S11',
        'frequency_column': 'Freq [GHz]',
        's11_column': 'dB(S(1,1)) []',
        'marker': '',
        'linestyle': '-',
        'color': 'red'
    }


    # Call the plot function with all three datasets
    plot_s11_datasets([measured_dataset_info, simulated_dataset_info], xlabel='Frequency (GHz)', ylabel='S11 (dB)', title='Measured vs Simulated S11 Data')
    # Plot horizontal line at -10 dB threshold
    plot_horizontal_line(
        y_value=-10,  # The y-coordinate where you want the horizontal line
        label='-10 dB Threshold',
        color='black',
        linestyle='--',
        linewidth=1
    )

    # Enable the grid
    plt.grid(True)

    # Set x-axis limits
    plt.xlim(2, 3)

    # Save the S11 plot to a PDF file
    plt.savefig("src/Img/T4/S11_real_vs_measured_short.pdf")
    logging.info("S11 plot saved to S11_real_vs_measured_short.pdf")
    
    

    # Convert spherical to Cartesian coordinates for 3D plotting

    radiation_data, gain_linear = load_radiation_pattern(file_path_radiation)
    x, y, z = spherical_to_cartesian(radiation_data['Theta[rad]'], radiation_data['Phi[rad]'], gain_linear)

    # Plot the radiation pattern in 3D
    plot_3d_radiation_pattern(x, y, z, c=gain_linear, cmap='inferno')
    logging.info("Radiation pattern plot completed.")
    
    plt.savefig("src/Img/T4/pattern.pdf")
    # Show the S11 plot
    plt.show()
    
     # Load the radiation pattern data
    data, gain_linear = load_radiation_pattern(file_path_radiation)

    # Approximate the integral over the solid angle
    integral_approx = integral_radiation_pattern(data, gain_linear)

    print(f"Approximation of Omega_a: {integral_approx:.4f}")
    print(f"Approximation of Directivity: {4*np.pi/integral_approx}")
    
# Call the main function
if __name__ == "__main__":
    main()
