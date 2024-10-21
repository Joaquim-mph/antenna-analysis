from utils import load_s11_data, plot_s11_datasets, plot_vertical_line, plot_horizontal_line, load_s11_parametric_data, plot_s11_parametric_data
import matplotlib.pyplot as plt


def main():
    # Load the S11 data from the first CSV file
    file_path1 = 'src/csv/s11_hole_45x70.csv'  # Update the path if necessary
    data1 = load_s11_data(
        file_path=file_path1,
        delimiter=',',
        decimal='.',  # Assuming decimal point is '.'
        frequency_column='Freq [GHz]',
        s11_column='dB(ActiveS(1:1)) []',
        frequency_factor=1  # Frequency is already in GHz
    )

    
    # Load the parametric S11 data
    file_path = 'src/csv/LxW_sweep.csv'  # Update the path if necessary
    frequency_column = 'Freq [GHz]'
    data, parameters = load_s11_parametric_data(
        file_path=file_path,
        delimiter=',',
        decimal='.',
        frequency_column=frequency_column)
    
    # Prepare dataset info for plotting
    datasets_info = [{
        'data': data1,
        'label': 'S11 Hole Patch Antenna',
        'frequency_column': 'Freq [GHz]',
        's11_column': 'dB(ActiveS(1:1)) []',
        'marker': '',
        'linestyle': '-',
        'color': 'red',
    }]
    
    
    # Plot the S11 data
    plot_s11_datasets(
        datasets_info,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title='S11 of Hole Patch Antenna')
    
        # Plot vertical lines where desired
    plot_vertical_line(
        x_value=2.15,  # The x-coordinate where you want the vertical line
        label='Design Frequency',
        color='black',
        linestyle='--',
        linewidth=1)

        # Plot horizontal lines where desired
    plot_horizontal_line(
        y_value=-10,  # The y-coordinate where you want the horizontal line
        label='-10 dB Threshold',
        color='navy',
        linestyle=':',
        linewidth=1
    )
    plt.savefig("src/img/hole.png")

    
    # Plot the S11 parametric data
    plot_s11_parametric_data(
        data=data,
        frequency_column=frequency_column,
        parameters=parameters,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title='S11 Parametric Analysis of Patch Dimensions'
    )
    plt.savefig("src/img/igualsi.png")

    
    
if __name__ == "__main__":
    main()