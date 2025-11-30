""" Smart fridge room simulation with brute force optimizer included """

import numpy as np
import Std_fridge_lib as std
import Smart_fridge_lib as smart


def main(debug_info=False):
    """
    Input: None

    Output: Prints the best cost found from monte carlo simulation with optimized goal temperatures

    Description: Start point for the fridge room simulation with smart thermostat.
    """

    # Electricity prices for all of September 2022, in 5 minute intervals
    price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])

    # Determine price intervals based on prices throughout September
    # Package them in array, then pass it to compressor_start to avoid recalculating them each time
    price_quantiles = [np.min(price), np.quantile(price, 0.25), np.mean(price), np.quantile(price, 0.75), np.max(price)]

    # Seed for random value
    np.random.seed(42)

    # Nearly brute force optimized goal temperatures
    g1=4.224 # 0% to 25%
    g2=5.465 # 25% to 50%
    g3=6.29  # 50% to 75%
    g4=6.29  # 75% to 100%

    # Amount of monte carlo simulations
    count = 100

    print(f"Beginning smart simulation with goal temps: {g1}, {g2}, {g3}, {g4}")

    if debug_info:
        # Perform monte carlo simulation with debug info
        simulations = monte_carlo(count, price, g1, g2, g3, g4, price_quantiles, debug_info)
        
        cost = 0
        for i in range(len(simulations)):
            # [ Monte_carlo , [food_waste.sum()+power_cost.sum(), T, power_cost, food_waste] ]
            cost = simulations[0]

        print(f"The average cost is given at {cost:.2f}")
        std.compare_to_budget(cost, 12000)
        return simulations
    else: 
        # Calculate average total cost for cooling room
        cost = monte_carlo(count, price, g1, g2, g3, g4, price_quantiles)
        print(f"The average cost is given at {cost:.2f}")
        std.compare_to_budget(cost, 12000)

def brute_force_optimizer():
    """
    This function is just like main(), but it brute forces the optimal values for compressor_start.
    Some optimisation was done, since its dumb to cool more when the price is higher.
    From this, it is trivial to set up a<b<c<d, 
    where a is the goal temperature for the cheapest interval up to d, for the expensive interval
    
    Note: 
    DO NOT RUN THIS CODE WHEN TESTING
    This function took about 3.5 hours to run, where 

    """

    # Electricity prices for all of September 2022, in 5 minute intervals
    price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])

    # Determine price intervals based on prices throughout September
    # Package them in array, then pass it to compressor_start to avoid recalculating them each time
    price_quantiles = [np.min(price), np.quantile(price, 0.25), np.mean(price), np.quantile(price, 0.75), np.max(price)]

    # Temperature bounds for goal temperatures
    min_temp = 3.5
    max_temp = 6.5

    # Which values id like it to run through
    temps = np.linspace(min_temp, max_temp, 30)

    # Seed for random value
    np.random.seed(42)
    count = 25

    # Very high initial best cost, to be beaten
    best_cost = 10000000

    # Initialize best goals as empty tuple to be filled later
    best_goals = (0, 0, 0, 0)

    # Begin brute forcing
    # Cheapest interval, a for g1
    for g1 in temps:
        # Progess bar for outer loop
        print(f"\nL1: {((g1 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g1:.2f}")

        # Second cheapest interval, b for g2
        for g2 in temps:
            # Progress bar for second loop
            print(f"L2: {((g2 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g2:.2f}")

            # Since a<b then g2 must be larger than g1. Therefore continue
            if g2 < g1:
                continue

            # Second most expensive interval, c for g3
            for g3 in temps:
                # Progress bar for third loop
                print(f"L3: {((g3 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g3:.2f}")

                # Since b<c then g3 must be larger than g2. Therefore continue
                if g3 < g2:
                    continue

                # Most expensive interval, d for g4
                for g4 in temps:

                    # Since c<d then g4 must be larger than g3. Therefore continue
                    if g4 < g3:
                        continue

                    # Calculate average total cost for cooling room with current goal temperatures
                    cost = monte_carlo(count, price, g1, g2, g3, g4, price_quantiles)

                    # If cost is better than best cost, store it
                    # Very importantly store the goal temperatures as well
                    if cost < best_cost:
                        best_cost = cost
                        best_goals = (g1, g2, g3, g4)
                    
    # When the brute forcing is done, print the best cost and the goal temperatures that achieved it
    print(f"The best cost is given at {best_cost}, for the parameter combo of {best_goals}")



def monte_carlo(count, price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles, debug_info=False):
    monte_carlo_sum = 0
    if debug_info:
        simulations = []
        for i in range(count):
            # Save current simulation result, along with all debug info
            result = fridge_room(price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles, debug_info)
            simulations.append(result)
            
            # [food_waste.sum()+power_cost.sum(), T, power_cost, food_waste] 
            monte_carlo_sum += result[0]
        return [monte_carlo_sum / count, simulations]
    else:
        for i in range(count):
            monte_carlo_sum += fridge_room(price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles)
    
        monte_carlo_average = monte_carlo_sum / count
        return monte_carlo_average

def fridge_room(price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles, debug_info=False):
    # Designate random value to define if the door is open or closed for each time interval
    door_open_chance_value = np.random.random(len(price))

    # Set up temperature array, filled with zeros, except the start condition, which is assumed to be 5
    T = np.zeros(len(price))
    T[0] = 5

    # Calculate if the door is open by applying the conditional to door_open_chance_value
    # Creates array of c_1 values for each time interval
    c_1 = np.where(door_open_chance_value < 0.1, 3e-5, 5e-7)


    # Constants
    T_rum = 20
    T_komp = -5
    Delta_t = 300

    # Initialize arrays to hold power cost and food waste
    power_cost = np.zeros(len(price))    
    food_waste = np.zeros(len(price))

    # Calculate each step of the way, what the temperature will be, without using i=0, as that is the starting condition
    for i in range(1, len(price)):
         # Determine if the compressor needs to be turned on, depending on temperature and current price
         c_2 = smart.compressor_start(price[i], T[i-1], goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles)

         T[i] = T[i-1] + (c_1[i]*(T_rum - T[i-1]) + c_2*(T_komp - T[i-1]))*Delta_t
    
         # Calculate food waste based on last temperature. Since thats how much was lost because of that temperature until this time interval
         current_food_waste = 4.39*np.exp(-0.49*T[i-1]) if T[i-1] < 3.5 else (0.11*np.exp(0.31*T[i-1]) if T[i-1] > 6.5 else 0)
         food_waste[i] = current_food_waste

         # Calculate power consumption based on if compressor was on
         power_cost[i] += price[i] if c_2 > 0 else 0
    
    if debug_info:
        return [food_waste.sum()+power_cost.sum(), T, power_cost, food_waste]
    else:
        # Return the total cost
        return food_waste.sum()+power_cost.sum()


# brute_force_optimizer()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()