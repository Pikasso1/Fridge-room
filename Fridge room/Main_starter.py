""" Main starter file for fridge room simulation. """

import numpy as np
import Fridge_room as std
import NP_Fridge_room as smart
import Plot_Grouper as grouper
import matplotlib.pyplot as plt

def UI():
    """
    Main entry point for the fridge room simulation.
    """
    # Boolean loops for UI, forces the user to input valid data
    Graphing_loop = True
    Simulation_loop = True

    while Graphing_loop:
        print("Would you like graphs or just the result?")
        plots_choice = input("Pick 'yes' for graphs, 'no' for results only:\n")

        if plots_choice == "yes":
            # Make sure that the user stops being asked for more input
            Graphing_loop = False

            plots()
        elif plots_choice == "no":
            # Make sure that the user stops being asked for more input
            Graphing_loop = False

            while Simulation_loop:
                print("Would you like to run only one simulation?\n")
                choice = input("Enter 'no' to run all simulations, else pick\n '1' - Simple thermostat\n '2' - Smart thermostat\n\n")

                if choice.lower() == 'no':
                    # Make sure that the user stops being asked for more input
                    Simulation_loop = False

                    # Run all simulations
                    smart.main()
                    std.main()
                elif choice == '1':
                    # Make sure that the user stops being asked for more input
                    Simulation_loop = False

                    # Run simple thermostat simulation
                    std.main()
                elif choice == '2':
                    # Make sure that the user stops being asked for more input
                    Simulation_loop = False

                    # Run smart thermostat simulation
                    smart.main()
                else:
                    # Invalid input, ask again
                    print("Invalid choice. Please enter 'no', '1', or '2'.")
        else:
            # Invalid input, ask again
            print("Invalid choice. Please enter 'yes' or 'no'.")

def grouped_plots():
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
    simple_data = std.main(debug_info=True) # # [ Monte_carlo , [tot_forbrug+tot_madtab, T, forbrug, madtab]]
    smart_data = smart.main(debug_info=True) # [ Monte_carlo , [food_waste.sum()+power_cost.sum(), T, power_cost, food_waste] ]

    # Make average arrays (length = number of timesteps)
    n_sims = len(simple_data[1])
    n_sims_smart = len(smart_data[1])
    n_steps = len(simple_data[1][0][1])   # T array length is the timestep count

    # Initialize average arrays - Simple
    average_total_price = 0.0                     # scalar average
    average_power_price = np.zeros(n_steps)       # array
    average_food_waste  = np.zeros(n_steps)       # array

    # Initialize average arrays - Smart
    average_total_price_smart = 0.0                     # scalar average
    average_power_price_smart = np.zeros(n_steps)       # array
    average_food_waste_smart  = np.zeros(n_steps)       # array

    # Loop over every simulation - Simple
    for i in range(n_sims):
        sim_total  = simple_data[1][i][0]   # scalar
        sim_T      = simple_data[1][i][1]   # array
        sim_power  = simple_data[1][i][2]   # array
        sim_food   = simple_data[1][i][3]   # array

        average_total_price += sim_total
        average_power_price += sim_power
        average_food_waste  += sim_food

    # Loop over every simulation - Smart
    for i in range(n_sims):
        sim_total  = smart_data[1][i][0]   # scalar
        sim_T      = smart_data[1][i][1]   # array
        sim_power  = smart_data[1][i][2]   # array
        sim_food   = smart_data[1][i][3]   # array

        average_total_price_smart += sim_total
        average_power_price_smart += sim_power
        average_food_waste_smart  += sim_food

    # Divide to get averages - Simple
    average_total_price /= n_sims
    average_power_price /= n_sims
    average_food_waste  /= n_sims

    # Divide to get averages - Smart
    average_total_price_smart /= n_sims_smart
    average_power_price_smart /= n_sims_smart
    average_food_waste_smart  /= n_sims_smart

    # Grouping the averaged out data for better plotting - Simple
    Power_price_grouped = grouper.group_data(average_power_price, grouping_factor)
    Food_waste_grouped  = grouper.group_data(average_food_waste, grouping_factor)

    # Grouping the averaged out data for better plotting - Smart
    Power_price_grouped_smart = grouper.group_data(average_power_price_smart, grouping_factor)
    Food_waste_grouped_smart  = grouper.group_data(average_food_waste_smart, grouping_factor)

    # Sanity check, calculate total price from grouped averaged data
    total_price_check = np.sum(Power_price_grouped) + np.sum(Food_waste_grouped)
    total_price_check_smart = np.sum(Power_price_grouped_smart) + np.sum(Food_waste_grouped_smart)

    # Print out the values just for debugging sanity check
    print(f"Total price from grouped averaged data: {total_price_check} DKK") #This should equal around 13750
    print(f"Total price from grouped averaged data (Smart): {total_price_check_smart} DKK") # This sould equal around 10800

    # Plot power price
    # plt.figure(figsize=(12, 6))
    plt.plot(x, Power_price_grouped, label="Simple - Power Price", color="orange")
    plt.plot(x, Power_price_grouped_smart, label="Smart - Power Price", color="blue")
    plt.title("Price of power used over time")
    plt.xlabel("Time")
    plt.ylabel("Price (DKK)")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot food waste
    #plt.figure(figsize=(12, 6))
    plt.plot(x, Food_waste_grouped, label="Simple - Food Waste", color="green")
    plt.plot(x, Food_waste_grouped_smart, label="Smart - Food Waste", color="red")
    plt.title("Food Waste over time (Simple Fridge Room)")
    plt.xlabel("Time")
    plt.ylabel("Food Waste (DKK)")
    plt.legend()
    plt.grid()
    plt.show()


    # print(f"Length of Power_price: {len(Power_price_grouped)}")
    # print(f"Length of Food_waste: {len(Food_waste_grouped)}")
    # print(f"Length of x: {len(x)}")

def plot(x, power_price, power_price_smart, food_waste, food_waste_smart):
    pass

#UI()
grouped_plots()

plots()