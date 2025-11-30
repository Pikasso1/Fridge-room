""" Simple fridge room simulation """

import random
import numpy as np

import Std_fridge_lib as std


def fridge_room(goal_temp, price, debug_info=False):
    """
    Input:
    Goal temperature - Float
    Price - Numpy array
    Debug info - Boolean

    Output:
    Total cost - Float
    simulation data - List of Numpy arrays if debug_info is True

    Description:
    Simulates a fridge room using September 2022 power price data using the given goal temperature.
    """

    tot_temp = 0
    T = np.zeros(len(price))
    forbrug = np.zeros(len(price))
    madtab = np.zeros(len(price))

    Temp_rum = 20
    Temp_komp = -5

    deltat = 300

    # Set start temperature to be 5
    T[0] = 5

    for i in range(1, len(price)):
        # Sum up total temperature for debugging
        tot_temp = tot_temp + T[i-1]

        # Generate random number and calculate if door is open
        r = random.random()
        c_1 = std.door_open(r)

        # Check if the compressor needs to be turned on, depending on goal temperature
        c_2 = std.compressor_start(T[i-1], goal_temp)

        # If its been turned on, then log the price of power at that moment
        if c_2 != 0:
            forbrug[i] = price[i]

        # Calculate new temperature
        T[i] = T[i-1] + (c_1*(Temp_rum - T[i-1]) + c_2*(Temp_komp - T[i-1]))*deltat
            
        # Calculate food waste at this temperature
        madtab[i] = std.food_waste(T[i])
    
    # Total power consumption cost and food waste cost
    tot_forbrug = forbrug.sum()
    tot_madtab = madtab.sum()

    # Return total cost for this simulation
    if debug_info:
        return [tot_forbrug+tot_madtab, T, forbrug, madtab]
    else:
        return tot_forbrug+tot_madtab

def monte_carlo_simple(count, goal_temp, price, debug_info=False):
    """
    Input:
    Count - Integer
    Goal temperature - Float
    Price - Numpy array
    Debug info - Boolean

    Output:
    Monte carlo average - Float
    simulations - List of simulation results if debug_info is True

    Description:
    Takes in the number of simulations to run, goal temperature, and price data, and 
    runs monte carlo simulations to find average cost to run fridge at that goal temperature
    """
    # Array to hold all simulation results
    simulations = []
    
    # If the debug info is wanted, return all results
    if debug_info:
        # Running total for monte carlo average
        monte_carlo_sum = 0

        # Run simulations
        for i in range(count):
            # Save current simulation result, along with all debug info
            simulations.append(fridge_room(goal_temp, price, True))
            monte_carlo_sum += simulations[i][0]

        # Calculate monte carlo average
        monte_carlo_average = monte_carlo_sum/count
        return [monte_carlo_average, simulations] # [ Monte_carlo , [tot_forbrug+tot_madtab, T, forbrug, madtab]]
    else:
        # Run simulations
        for i in range(count):
            # Save current simulation result, without debug info
            simulations.append(fridge_room(goal_temp, price))

        # Calculate monte carlo average
        monte_carlo_average = sum(simulations)/count
        return monte_carlo_average


def main(debug_info=False):
    """
    Input:
    debug_info - Boolean

    Output:
    simulations - List of simulation results if debug_info is True

    Description:
    Main function to run monte carlo simulation at a set goal temperature and compare to budget
    """
    # Read in price data
    price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])
    print("Beginning simple simulation with goal temp 5")

    if debug_info:
        # Perform monte carlo simulation with debug info
        simulations = monte_carlo_simple(100, 5.0, price, debug_info)

        average_cost = simulations[0]

        # Print average cost
        print(f"Average cost is given at: {average_cost:.2f}")
    
        # Compare to budget of 12000
        std.compare_to_budget(average_cost, 12000)

        return simulations # [ Monte_carlo , [tot_forbrug+tot_madtab, T, forbrug, madtab]]
    else: 
        # Perform monte carlo simulation at goal temperature of 5.0 degrees
        average_cost = monte_carlo_simple(100, 5.0, price)

        # Print average cost
        print(f"Average cost is given at: {average_cost}")
    
        # Compare to budget of 12000
        std.compare_to_budget(average_cost, 12000)

