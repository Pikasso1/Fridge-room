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