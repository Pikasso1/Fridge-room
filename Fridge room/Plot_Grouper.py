"""Module to group numerical data in a numpy array by a specified factor."""

import numpy as np

def group_data(numerical_array, grouping_factor):
    """
    Input:
    numerical_array - Numpy array
    grouping_factor - Integer

    Output:
    grouped_array - Numpy array
    
    Description:
    Groups data in the input numerical array by the given grouping factor.
    """
    # Calculate the size of the grouped array
    num_groups = len(numerical_array) // grouping_factor

    # Initialize the grouped array
    grouped_array = np.zeros(num_groups)

    # Group and average the data
    for index in range(len(numerical_array)):
        grouped_array[index // grouping_factor] += numerical_array[index]
        
    return grouped_array

def sum_curve_data_generator(array):
    """
    Input:
    array - Numpy array

    Output:
    summed_array - Numpy array

    Description:
    Generates a running sum curve from the input array.
    Each element in the output array is the sum of all previous elements in the input array up to that index.
    """
    summed_array = np.zeros(len(array))
    running_total = 0.0
    for i in range(len(array)):
        running_total += array[i]
        summed_array[i] = running_total
    return summed_array