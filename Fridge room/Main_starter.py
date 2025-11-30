import numpy as np
import Fridge_room as std
import Smart_fridge_lib as smart
import Plot_Grouper as grouper

import matplotlib.pyplot as plt

def main():
    std.main()
    
def plots():
    """
    Input: None

    Output:
    Plots - Matplotlib plots

    Description:
    Generates plots for the smart fridge room simulation.
    """

    # Domain for x-axis
    grouping_factor = 12*6  # 1 hour intervals
    x = range(0, int(30*24*60/5), grouping_factor)

    # Load simulation data from simple fridge room
    simple_data = std.main(debug_info=True)

    # Sort out data
    Total_price = simple_data[1][50][0] # total price at simulation 50
    Power_price = simple_data[1][50][2] # power price at simulation 50
    Food_waste  = simple_data[1][50][3] # food waste data at simulation 50

    # Make average arrays (length = number of timesteps)
    n_sims = len(simple_data[1])
    n_steps = len(simple_data[1][0][1])   # T array length is the timestep count

    average_total_price = 0.0                     # scalar average
    average_power_price = np.zeros(n_steps)
    average_food_waste  = np.zeros(n_steps)

    # Loop over every simulation
    for i in range(n_sims):
        sim_total  = simple_data[1][i][0]   # scalar
        sim_T      = simple_data[1][i][1]   # array
        sim_power  = simple_data[1][i][2]   # array
        sim_food   = simple_data[1][i][3]   # array

        average_total_price += sim_total
        average_power_price += sim_power
        average_food_waste  += sim_food

    # Divide to get averages
    average_total_price /= n_sims
    average_power_price /= n_sims
    average_food_waste  /= n_sims


    # Group data for better plotting
    # Power_price_grouped = grouper.group_data(Power_price, grouping_factor)
    # Food_waste_grouped  = grouper.group_data(Food_waste, grouping_factor)

    # Grouping the averaged out data for better plotting
    Power_price_grouped = grouper.group_data(average_power_price, grouping_factor)
    Food_waste_grouped  = grouper.group_data(average_food_waste, grouping_factor)

    # Sanity check, calculate total price from grouped averaged data
    total_price_check = np.sum(Power_price_grouped) + np.sum(Food_waste_grouped)

    #This should equal around 11400
    print(f"Total price from grouped averaged data: {total_price_check} DKK")

    # Plot power price
    # plt.figure(figsize=(12, 6))
    plt.plot(x, Power_price_grouped, label="Power Price", color="orange")
    plt.plot()
    plt.title("Price of power used over time (Simple Fridge Room)")
    plt.xlabel("Time (5 minute intervals)")
    plt.ylabel("Price (DKK)")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot food waste
    plt.figure(figsize=(12, 6))
    plt.plot(x, Food_waste_grouped, label="Food Waste", color="green")
    plt.title("Food Waste over time (Simple Fridge Room)")
    plt.xlabel("Time (five minute intervals)")
    plt.ylabel("Food Waste (DKK)")
    plt.legend()
    plt.grid()
    plt.show()


    # print(f"Length of Power_price: {len(Power_price_grouped)}")
    # print(f"Length of Food_waste: {len(Food_waste_grouped)}")
    # print(f"Length of x: {len(x)}")

# main()
plots()