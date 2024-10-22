import matplotlib.pyplot as plt
from utils import (
    load_s11_data,
    load_s11_parametric_data,
    load_and_filter_s11_data,
    plot_s11_datasets,
    plot_s11_parametric_data,
    plot_filtered_s11_data,
    plot_vertical_line,
    plot_horizontal_line
)



def main():
    # Load the S11 data from the first CSV file
    file_path1 = 'src/csv/pabloT4/medido_2_10Ghz.csv'  # Update the path if necessary
    data1 = load_s11_data(
        file_path=file_path1,
        delimiter=',',
        decimal='.',  # Assuming decimal point is '.'
        frequency_column='Frequency',
        s11_column='dB(ActiveS(1:1)) []',
        frequency_factor=1  # Frequency is already in GHz
    )

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
        title='S11 of Hole Patch Antenna'
    )
    
    # Plot vertical line at design frequency
    plot_vertical_line(
        x_value=2.15,  # The x-coordinate where you want the vertical line
        label='Design Frequency',
        color='black',
        linestyle='--',
        linewidth=1
    )

    # Plot horizontal line at -10 dB threshold
    plot_horizontal_line(
        y_value=-10,  # The y-coordinate where you want the horizontal line
        label='-10 dB Threshold',
        color='navy',
        linestyle=':',
        linewidth=1
    )
    
    # Show the plot
    plt.show()
    
    # Load the parametric S11 data
    file_path = 'src/csv/LxW_sweep.csv'  # Update the path if necessary
    frequency_column = 'Freq [GHz]'
    data, parameters = load_s11_parametric_data(
        file_path=file_path,
        delimiter=',',
        decimal='.',
        frequency_column=frequency_column
    )
    
    # Plot the S11 parametric data
    plot_s11_parametric_data(
        data=data,
        frequency_column=frequency_column,
        parameters=parameters,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title='S11 Parametric Analysis of Patch Dimensions'
    )
    # Optionally save the figure
    # plt.savefig("src/img/igualsi.png")
    
    # Show the plot
    plt.show()
    
    # Load and filter the parametric S11 data
    path_big_parametric = 'src/csv/big_parametric.csv'  # Update the path to your CSV file
    frequency_column = 'Freq [GHz]'
    s11_threshold = -10  # S11 threshold in dB

    data, filtered_parameters = load_and_filter_s11_data(
        file_path=path_big_parametric,
        delimiter=',',
        decimal='.',
        frequency_column=frequency_column,
        s11_threshold=s11_threshold
    )

    # Plot the filtered S11 data
    plot_filtered_s11_data(
        data=data,
        frequency_column=frequency_column,
        filtered_parameters=filtered_parameters,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title=f'S11 Datasets with S11 ≤ {s11_threshold} dB'
    )
    
    # Show the plot
    plt.show()
    
if __name__ == "__main__":
    main()