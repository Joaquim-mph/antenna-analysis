import pandas as pd
import logging
from utils import *
import os

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Define the paths to the CSV files
    file_path_measured = 'src/csv/pabloT4/medido_2_10Ghz.csv'
    file_path_simulated = 'src/csv/pabloT4/S11_simulado_6GHz.csv'

    # Check if the measured file exists
    if not os.path.exists(file_path_measured):
        logging.error(f"File {file_path_measured} does not exist.")
        return
    
    # Check if the simulated file exists
    if not os.path.exists(file_path_simulated):
        logging.error(f"File {file_path_simulated} does not exist.")
        return

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

    # Call the plot function with both datasets
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
    plt.xlim(2, None)
    
    # Save the plot to a PDF file
    output_file = "S11_real_vs_measured.pdf"
    plt.savefig(output_file)
    logging.info(f"Plot saved to {output_file}")
    
    # Show the plot
    plt.show()

# Call the main function
if __name__ == "__main__":
    main()


