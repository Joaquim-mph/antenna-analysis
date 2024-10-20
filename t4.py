from utils import load_s11_data, plot_s11_datasets, plot_vertical_line, plot_horizontal_line, load_s11_parametric_data, plot_s11_parametric_data
import matplotlib.pyplot as plt


def main():
    # Load the S11 data from the first CSV file
    file_path1 = 'src/csv/s11_opt1_patch.csv'  # Update the path if necessary
    data1 = load_s11_data(
        file_path=file_path1,
        delimiter=',',
        decimal='.',  # Assuming decimal point is '.'
        frequency_column='Freq [GHz]',
        s11_column='dB(ActiveS(1:1)) []',
        frequency_factor=1  # Frequency is already in GHz
    )

    # Load the S11 data from the second CSV file
    file_path2 = 'src/csv/s11_simple_patch.csv'  # Update the path if necessary
    data2 = load_s11_data(
        file_path=file_path2,
        delimiter=',',
        decimal='.',  # Assuming decimal point is '.'
        frequency_column='Freq [GHz]',
        s11_column='dB(ActiveS(1:1)) []',
        frequency_factor=1  # Frequency is already in GHz
    )
    
    # Load the parametric S11 data
    file_path = 'src/csv/s11_parametric_length.csv'  # Update the path if necessary
    frequency_column = 'Freq [GHz]'
    data, largo_parche_columns, largo_parche_values = load_s11_parametric_data(
        file_path=file_path,
        delimiter=',',
        decimal='.',
        frequency_column=frequency_column
    )
    
    # Prepare dataset info for plotting
    datasets_info = [
        {
            'data': data1,
            'label': 'S11 optimized Simple Patch Antenna',
            'frequency_column': 'Freq [GHz]',
            's11_column': 'dB(ActiveS(1:1)) []',
            'marker': '',
            'linestyle': '-',
            'color': 'red',
        },
        {
            'data': data2,
            'label': 'S11 Simplest Patch',
            'frequency_column': 'Freq [GHz]',
            's11_column': 'dB(ActiveS(1:1)) []',
            'marker': '',
            'linestyle': '--',
            'color': 'teal',
        }
    ]
    
    # Plot the S11 data
    plot_s11_datasets(
        datasets_info,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title='S11 of Patch Antenna V1 and V2')
    
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
    # Plot the S11 parametric data
    plot_s11_parametric_data(
        data=data,
        frequency_column=frequency_column,
        largo_parche_columns=largo_parche_columns,
        largo_parche_values=largo_parche_values,
        xlabel='Frequency (GHz)',
        ylabel='S11 (dB)',
        title='S11 Parametric Analysis of Patch Length'
    )
    plt.show()
    
    
if __name__ == "__main__":
    main()