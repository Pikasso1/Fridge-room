""" Holds standard functions for fridge room simulations """

import math
import numpy as np

def door_open(random):
    """
    Input:
    Random value r - Float

    Return:
    C_1 - Float

    Description:
    Takes in a random value, and determines if the door is open

    # Under and equal 10% - Door open
    >>> round(door_open(0.05),10)
    3e-05

    # Over 10% - Door closed
    >>> round(door_open(0.5),10)
    5e-07
    """
    if random <= 0.1:
        return 3*10**(-5)
    else:
        return 5*10**(-7)

def compressor_start(current_temp, goal_temp):
    """
    Input:
    Current temperature - Float
    Goal temperature - Float

    Output:
    C_2 - Float

    Description:
    Takes in the current temperature and goal temperature, and determines if the compressor needs to be started

    # Current temperature above goal temperature - Compressor on
    >>> round(compressor_start(7, 5),10)
    8e-06

    # Current temperature below goal temperature - Compressor off
    >>> round(compressor_start(3, 5),10)
    0
    """
    if current_temp > goal_temp:
        return 8*10**(-6)
    else:
        return 0

def food_waste(current_temp):
    """
    Input:
    Temperature - Float

    Output:
    Food waste - Float

    Description:
    Takes in the temperature and calculates food waste based on it

    # Temperature below 3.5 degrees
    >>> round(food_waste(2),10)
    1.647615724

    # Temperature above 6.5 degrees
    >>> round(food_waste(7),10)
    0.9634112445

    # Temperature between 3.5 and 6.5 degrees
    >>> round(food_waste(5),10)
    0
    """
    if current_temp < 3.5:
        return 4.39*math.exp(-0.49*current_temp)
    elif current_temp > 6.5:
        return 0.11*math.exp(0.31*current_temp)
    else:
        return 0

def goal_temp_optimization():
    """
    Input:
    None

    Output:
    None

    Description:
    Prints the optimal goal temperature found through brute force check
    """
    # Read in price data
    price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])

    # Generate temperature range to test
    temperatures = np.linspace(3.5, 6.5, num=31)

    # Initialize best guess variables
    best_guess = 0
    best_temp = 0

    # Test each temperature in the range
    for goal_temp in temperatures:
        # Perform monte carlo simulation for current goal temperature
        # Average is needed to reduce randomness
        gennemsnit_omkostninger = monte_carlo_simple(100, goal_temp, price)

        # Update best guess if current is better
        if gennemsnit_omkostninger < best_guess or best_guess == 0:
            best_guess = gennemsnit_omkostninger
            best_temp = goal_temp

    # Print the best found goal temperature and its associated cost
    print(f"\nExpenses given as: {best_guess} at the temp {best_temp}")

def compare_to_budget(average_cost, budget):
    """
    Input:
    average_cost - Float
    budget - Float

    Output:
    void

    Description:
    Compares the average cost to the budget and prints the result

    # Average cost within budget
    >>> compare_to_budget(11000, 12000)
    The average cost of 11000 is within the budget of 12000 by 1000.

    # Average cost exceeds budget
    >>> compare_to_budget(13000, 12000)
    The average cost of 13000 is exceeds the budget of 12000 by 1000.

    # Unexpected error case
    >>> compare_to_budget(float('nan'), 12000)
    An unexpected error occurred during budget comparison.
    """
    if average_cost <= budget:
        print(f"The average cost of {average_cost:.2f} is within the budget of {budget} by {budget - average_cost:.2f}.\n")
    elif average_cost > budget:
        print(f"The average cost of {average_cost:.2f} exceeds the budget of {budget} by {average_cost - budget:.2f}.\n")
    else:
        print("An unexpected error occurred during budget comparison.\n")

if __name__ == "__main__":
    import doctest
    doctest.testmod()