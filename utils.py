import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import re


def load_s11_data(file_path, delimiter=',', decimal='.', frequency_column='Frequency', s11_column='S11-Gain (dB)', frequency_factor=1):
    """
    Load S11 data from a CSV file.

    Parameters:
    - file_path: path to the CSV file.
    - delimiter: delimiter used in the CSV file.
    - decimal: decimal point character in the CSV file.
    - frequency_column: name of the frequency column.
    - s11_column: name of the S11 column.
    - frequency_factor: factor to apply to frequency data (e.g., to convert units).

    Returns:
    - data: pandas DataFrame with the loaded data.
    """
    data = pd.read_csv(file_path, delimiter=delimiter, decimal=decimal)
    data[frequency_column] = pd.to_numeric(data[frequency_column]) * frequency_factor
    return data

def plot_vertical_line(x_value, label=None, color='red', linestyle='--', linewidth=1):
    """
    Plot a vertical line at a specified x-coordinate.

    Parameters:
    - x_value: x-coordinate where the vertical line is drawn.
    - label: (optional) label for the vertical line.
    - color: (optional) color of the line.
    - linestyle: (optional) line style.
    - linewidth: (optional) width of the line.
    """
    plt.axvline(x=x_value, color=color, linestyle=linestyle, linewidth=linewidth, label=label)

def plot_horizontal_line(y_value, label=None, color='blue', linestyle='--', linewidth=1):
    """
    Plot a horizontal line at a specified y-coordinate.

    Parameters:
    - y_value: y-coordinate where the horizontal line is drawn.
    - label: (optional) label for the horizontal line.
    - color: (optional) color of the line.
    - linestyle: (optional) line style.
    - linewidth: (optional) width of the line.
    """
    plt.axhline(y=y_value, color=color, linestyle=linestyle, linewidth=linewidth, label=label)


def plot_s11_datasets(datasets_info, xlabel='Frequency (MHz)', ylabel='S11 (dB)', title=None):
    """
    Plot multiple S11 datasets on the same figure.

    Parameters:
    - datasets_info: list of dictionaries, each containing:
        - data: pandas DataFrame with the dataset.
        - label: label for the dataset.
        - frequency_column: name of the frequency column.
        - s11_column: name of the S11 column.
        - marker: (optional) marker style.
        - linestyle: (optional) line style.
        - color: (optional) line color.
    - xlabel: label for the x-axis.
    - ylabel: label for the y-axis.
    - title: (optional) title of the plot.
    """
    plt.figure(figsize=(7, 5))
    for info in datasets_info:
        data = info['data']
        label = info.get('label', '')
        freq_col = info['frequency_column']
        s11_col = info['s11_column']
        marker = info.get('marker', '')
        linestyle = info.get('linestyle', '')
        color = info.get('color', None)
        plt.plot(data[freq_col], data[s11_col], marker=marker, linestyle=linestyle, label=label, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.grid(False)
    plt.legend()

def load_s11_parametric_data(file_path, delimiter=',', decimal='.', frequency_column='Freq [GHz]'):
    """
    Load S11 parametric data from a CSV file.

    Parameters:
    - file_path: path to the CSV file.
    - delimiter: delimiter used in the CSV file.
    - decimal: decimal point character in the CSV file.
    - frequency_column: name of the frequency column.

    Returns:
    - data: pandas DataFrame with the loaded data.
    - parameter_columns: list of column names for different parameter combinations.
    - parameters: list of dictionaries containing 'ancho_parche' and 'largo_parche' values.
    """
    data = pd.read_csv(file_path, delimiter=delimiter, decimal=decimal)

    # Ensure the frequency column is numeric and properly scaled
    data[frequency_column] = pd.to_numeric(data[frequency_column])

    # Extract parameter columns
    parameter_columns = [col for col in data.columns if col != frequency_column]
    parameters = []
    pattern = r"ancho_parche='(\d+\.?\d*)mm' largo_parche='(\d+\.?\d*)mm'"

    for col in parameter_columns:
        match = re.search(pattern, col)
        if match:
            ancho_parche = float(match.group(1))
            largo_parche = float(match.group(2))
            parameters.append({'column': col, 'ancho_parche': ancho_parche, 'largo_parche': largo_parche})
        else:
            parameters.append({'column': col, 'ancho_parche': None, 'largo_parche': None})

    return data, parameters

def plot_s11_parametric_data(data, frequency_column, parameters, xlabel='Frequency (GHz)', ylabel='S11 (dB)', title=None):
    """
    Plot S11 parametric data.

    Parameters:
    - data: pandas DataFrame containing the data.
    - frequency_column: name of the frequency column.
    - parameters: list of dictionaries containing parameter info for each column.
    - xlabel: label for the x-axis.
    - ylabel: label for the y-axis.
    - title: (optional) title of the plot.
    """
    plt.figure(figsize=(10, 7))

    # Sort parameters by 'ancho_parche' and 'largo_parche'
    parameters_sorted = sorted(parameters, key=lambda x: (x['ancho_parche'], x['largo_parche']))

    # Get unique 'ancho_parche' and 'largo_parche' values
    ancho_parche_values = sorted(set(p['ancho_parche'] for p in parameters_sorted if p['ancho_parche'] is not None))
    largo_parche_values = sorted(set(p['largo_parche'] for p in parameters_sorted if p['largo_parche'] is not None))

    colors = cm.get_cmap('viridis', len(ancho_parche_values))
    linestyles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D']

    # Map 'ancho_parche' to colors
    ancho_parche_to_color = {ap: colors(i) for i, ap in enumerate(ancho_parche_values)}

    # Map 'largo_parche' to line styles or markers
    largo_parche_to_linestyle = {lp: linestyles[i % len(linestyles)] for i, lp in enumerate(largo_parche_values)}
    largo_parche_to_marker = {lp: markers[i % len(markers)] for i, lp in enumerate(largo_parche_values)}

    for p in parameters_sorted:
        col = p['column']
        ancho_parche = p['ancho_parche']
        largo_parche = p['largo_parche']
        if ancho_parche is not None and largo_parche is not None:
            color = ancho_parche_to_color[ancho_parche]
            linestyle = largo_parche_to_linestyle[largo_parche]
            marker = largo_parche_to_marker[largo_parche]
            label = f"W={int(ancho_parche)}mm, L={int(largo_parche)}mm"
            plt.plot(
                data[frequency_column], data[col], label=label, color=color,
                linestyle=linestyle, marker=marker, markevery=2, linewidth=1
            )
        else:
            plt.plot(data[frequency_column], data[col], label=col)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()


def load_radiation_pattern(file_path, phi_column='Phi[deg]', theta_column='Theta[deg]', gain_column='dB10normalize(GainTotal)'):
    """
    Load radiation pattern data from a CSV file.

    Parameters:
    - file_path: path to the CSV file.
    - phi_column: name of the phi (azimuthal angle) column in degrees.
    - theta_column: name of the theta (polar angle) column in degrees.
    - gain_column: name of the gain column in dB.

    Returns:
    - data: pandas DataFrame with the loaded data, including 'Phi[rad]' and 'Theta[rad]' columns.
    - gain_linear: numpy array with the gain values converted to linear scale.
    """
    data = pd.read_csv(file_path)
    data['Phi[rad]'] = np.radians(data[phi_column])
    data['Theta[rad]'] = np.radians(data[theta_column])
    gain_linear = 10 ** (data[gain_column] / 10.0)
    return data, gain_linear

def spherical_to_cartesian(theta_rad, phi_rad, r):
    """
    Convert spherical coordinates to Cartesian coordinates.

    Parameters:
    - theta_rad: numpy array of theta angles in radians.
    - phi_rad: numpy array of phi angles in radians.
    - r: numpy array of radial distances.

    Returns:
    - x, y, z: numpy arrays of Cartesian coordinates.
    """
    x = r * np.sin(theta_rad) * np.cos(phi_rad)
    y = r * np.sin(theta_rad) * np.sin(phi_rad)
    z = r * np.cos(theta_rad)
    return x, y, z

def plot_3d_radiation_pattern(x, y, z, c, cmap='viridis'):
    """
    Plot a 3D radiation pattern.

    Parameters:
    - x, y, z: numpy arrays of Cartesian coordinates.
    - c: numpy array of values used for coloring the points (e.g., gain).
    - cmap: colormap to use for the scatter plot.
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x, y, z, c=c, cmap=cmap)
    plt.colorbar(sc, ax=ax)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
