""" Main starter file for fridge room simulation. """

import numpy as np
import Fridge_room as std
import NP_Fridge_room as smart
import Plot_Grouper as grouper
import matplotlib.pyplot as plt
import os
import sys

def UI():
    """
    Main entry point for the fridge room simulation.
    """
    # Boolean loops for UI, forces the user to input valid data
    Graphing_loop = True
    Grouping_loop = True
    Simulation_loop = True

    while Graphing_loop:
        print("Would you like graphs or just the result?")
        plots_choice = input("Pick 'yes' for graphs, 'no' for results only:\n")
        clear()

        if plots_choice == "yes":
            # Make sure that the user stops being asked for more input
            Graphing_loop = False

            while Grouping_loop:
                graph_type = input("How would you like the data to be displayed?\n'1' - Sum curve\n'2' - No grouping\n'3' - 1 hour grouping\n'4' - 6 hour grouping\n'5' - 24 hour grouping\n")
                clear()
                if graph_type == "1":
                    Grouping_loop = False
                    grouped_plots(1, True)
                elif graph_type == "2":
                    Grouping_loop = False
                    grouped_plots(1)
                elif graph_type == "3":
                    Grouping_loop = False
                    grouped_plots(60/5)
                elif graph_type == "4":
                    Grouping_loop = False
                    grouped_plots(6*60/5)
                elif graph_type == "5":
                    Grouping_loop = False
                    grouped_plots(24*60/5)
                else:
                    print("Invalid input, please pick between 1 and 5\n")

        elif plots_choice == "no":
            # Make sure that the user stops being asked for more input
            Graphing_loop = False

            while Simulation_loop:
                print("Would you like to run only one simulation?\n")
                choice = input("Enter 'no' to run all simulations, else pick\n '1' - Simple thermostat\n '2' - Smart thermostat\n\n")
                clear()

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

def grouped_plots(grouping_factor, sum=False):
    """
    Input: 
    grouping_factor - Integer

    Output:
    Plots - Matplotlib plots

    Description:
    Generates plots for the smart fridge room simulation.
    Groups data by the given grouping factor for better visualization.
    """

    # Force interger, since division always returns float
    grouping_factor = int(grouping_factor)

    # Domain for x-axis
    x = range(0, int(30*24*60/5), grouping_factor)

    # Load simulation data from fridge rooms
    simple_data = std.main(debug_info=True) # # [ Monte_carlo , [tot_forbrug+tot_madtab, T, forbrug, madtab]]
    smart_data = smart.main(debug_info=True) # [ Monte_carlo , [food_waste.sum()+power_cost.sum(), T, power_cost, food_waste] ]

    # Make average arrays (length = number of timesteps)
    n_sims = len(simple_data[1])
    n_sims_smart = len(smart_data[1])
    n_steps = len(simple_data[1][0][1])   # T array length is the timestep count

    # Initialize average arrays - Simple
    average_total_price = 0.0                     # scalar average
    average_temp        = np.zeros(n_steps)       # array
    average_power_price = np.zeros(n_steps)       # array
    average_food_waste  = np.zeros(n_steps)       # array

    # Initialize average arrays - Smart
    average_total_price_smart = 0.0                     # scalar average
    average_temp_smart        = np.zeros(n_steps)       # array
    average_power_price_smart = np.zeros(n_steps)       # array
    average_food_waste_smart  = np.zeros(n_steps)       # array

    # Loop over every simulation - Simple
    for i in range(n_sims):
        sim_total  = simple_data[1][i][0]   # scalar
        sim_T      = simple_data[1][i][1]   # array
        sim_power  = simple_data[1][i][2]   # array
        sim_food   = simple_data[1][i][3]   # array

        average_temp        += sim_T
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
        average_temp_smart        += sim_T
        average_power_price_smart += sim_power
        average_food_waste_smart  += sim_food

    # Divide to get averages - Simple
    average_temp        /= n_sims
    average_total_price /= n_sims
    average_power_price /= n_sims
    average_food_waste  /= n_sims

    # Divide to get averages - Smart
    average_temp_smart        /= n_sims_smart
    average_total_price_smart /= n_sims_smart
    average_power_price_smart /= n_sims_smart
    average_food_waste_smart  /= n_sims_smart

    # Group data if grouping factor is more than 1
    if grouping_factor == 1:
        # Simple
        Temperature_grouped = average_temp
        Total_price_grouped = average_total_price
        Power_price_grouped = average_power_price
        Food_waste_grouped  = average_food_waste

        # Smart
        Temperature_grouped_smart = average_temp_smart
        Total_price_grouped_smart = average_total_price_smart
        Power_price_grouped_smart = average_power_price_smart
        Food_waste_grouped_smart  = average_food_waste_smart
        
    else:
        # Grouping the averaged out data for better plotting - Simple
        # Total_price_grouped = grouper.group_data(average_total_price, grouping_factor)
        # Temperature_grouped = grouper.group_data(average_temp, grouping_factor)
        Temperature_grouped = average_temp
        Power_price_grouped = grouper.group_data(average_power_price, grouping_factor)
        Food_waste_grouped  = grouper.group_data(average_food_waste, grouping_factor)

        # Grouping the averaged out data for better plotting - Smart
        # Total_price_grouped_smart = grouper.group_data(average_total_price_smart, grouping_factor)
        # Temperature_grouped_smart = grouper.group_data(average_temp_smart, grouping_factor)
        Temperature_grouped_smart = average_temp_smart
        Power_price_grouped_smart = grouper.group_data(average_power_price_smart, grouping_factor)
        Food_waste_grouped_smart  = grouper.group_data(average_food_waste_smart, grouping_factor)

        # Sanity check, calculate total price from grouped averaged data
        total_price_check = np.sum(Power_price_grouped) + np.sum(Food_waste_grouped)
        total_price_check_smart = np.sum(Power_price_grouped_smart) + np.sum(Food_waste_grouped_smart)

        # Print out the values just for debugging sanity check
        print(f"Total price from grouped averaged data: {total_price_check} DKK") #This should equal around 13750
        print(f"Total price from grouped averaged data (Smart): {total_price_check_smart} DKK") # This sould equal around 10800

    # Plot the data
    if sum:
        # Plot cumulative sum data
        plot_sum(x, Power_price_grouped, Power_price_grouped_smart, Food_waste_grouped, Food_waste_grouped_smart)
    else:
        # Plot normal data
        plot(x, Power_price_grouped, Power_price_grouped_smart, Food_waste_grouped, Food_waste_grouped_smart, grouping_factor, Temperature_grouped, Temperature_grouped_smart)


    # print(f"Length of Power_price: {len(Power_price_grouped)}")
    # print(f"Length of Food_waste: {len(Food_waste_grouped)}")
    # print(f"Length of x: {len(x)}")

def plot(x, power_price, power_price_smart, food_waste, food_waste_smart, grouping_factor,  temp=[1], temp_smart=[1]):
    """
    Input:
    x - Range for x-axis
    power_price - Numpy array of power price data (Simple)
    power_price_smart - Numpy array of power price data (Smart)
    food_waste - Numpy array of food waste data (Simple)
    food_waste_smart - Numpy array of food waste data (Smart)
    
    Output:
    Plots - Matplotlib plots
    
    Description:
    Generates plots for the smart fridge room simulation.
    """
    budget_line_y_values = [12000/len(x) for i in x]
    x_temp = [i for i in range(8640)]

    time_intervals = f"Time ({5} minute intervals)" # grouping_factor*5
    graph_title_power = f"Price of power used over time ({grouping_factor*5} minute interval groups)"
    graph_title_food  = f"Food Waste over time ({grouping_factor*5} minute interval groups)"
    graph_title_temp  = f"Temperature over time"

    # Plot power price
    # plt.figure(figsize=(12, 6))
    plt.plot(x, power_price, label="Simple - Power Price", color="orange")
    plt.plot(x, power_price_smart, label="Smart - Power Price", color="blue")
    plt.plot(x, budget_line_y_values, label="Budget Line", color="black", linestyle="--")
    plt.title(graph_title_power)
    plt.xlabel(time_intervals)
    plt.ylabel("Price (DKK)")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot food waste
    #plt.figure(figsize=(12, 6))
    plt.plot(x, food_waste, label="Simple - Food Waste", color="green")
    plt.plot(x, food_waste_smart, label="Smart - Food Waste", color="red")
    plt.title(graph_title_food)
    plt.xlabel(time_intervals)
    plt.ylabel("Food Waste (DKK)")
    plt.legend()
    plt.grid()
    plt.show()

    # Plot temperature
    #plt.figure(figsize=(12, 6))
    plt.plot(x_temp, temp, label="Simple - Food Waste", color="green")
    plt.plot(x_temp, temp_smart, label="Smart - Food Waste", color="red")
    plt.title(graph_title_temp)
    plt.xlabel(time_intervals)
    plt.ylabel("Average temperature in grouping (°C)")
    plt.legend()
    plt.grid()
    plt.show()

def plot_sum(x, power_price, power_price_smart, food_waste, food_waste_smart):
    """
    Input:
    x - Range for x-axis
    power_price - Numpy array of power price data (Simple)
    power_price_smart - Numpy array of power price data (Smart)
    food_waste - Numpy array of food waste data (Simple)
    food_waste_smart - Numpy array of food waste data (Smart)

    Output:
    Plots - Matplotlib plots

    Description:
    Generates cumulative sum plots for the fridge room simulations.
    """
    sum_power_price = grouper.sum_curve_data_generator(power_price)
    sum_power_price_smart = grouper.sum_curve_data_generator(power_price_smart)
    sum_food_waste = grouper.sum_curve_data_generator(food_waste)
    sum_food_waste_smart = grouper.sum_curve_data_generator(food_waste_smart)

    plot(x, sum_power_price, sum_power_price_smart, sum_food_waste, sum_food_waste_smart, 1)

def clear():
    """
    Way of clearing the terminal using cls for windows and clear for other operating systems

    If that doesnt do it, then force an ANSI escape character and flush the terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


UI()
# 6*60/5 = 6 hour intervals
# grouped_plots(1, False)
