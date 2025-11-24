import numpy as np

price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])

def main():
    

    min_temp = 3.5
    max_temp = 6.5

    # Which values id like it to run through
    temps = np.linspace(min_temp, max_temp, 30)

    # Seed for random value
    np.random.seed(42)
    count = 25

    best_cost = 10000000
    best_goals = (0, 0, 0, 0)

    for g1 in temps:
        print(f"\nL1: {((g1 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g1:.2f}")

        for g2 in temps:
            print(f"L2: {((g2 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g2:.2f}")
            if g2 < g1:
                continue
            for g3 in temps:
                print(f"L3: {((g3 - min_temp) / (max_temp - min_temp) * 100):5.1f}% done - We have now reached the temp {g3:.2f}")
                if g3 < g2:
                    continue
                for g4 in temps:
                    if g4 < g3:
                        continue

                    cost = monte_carlo(count, price, g1, g2, g3, g4)

                    if cost < best_cost:
                        best_cost = cost
                        best_goals = (g1, g2, g3, g4)
                    
    
    print(f"The best cost is given at {best_cost}, for the parameter combo of {best_goals}")

def monte_carlo(count, price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4):
    monte_carlo_sum = 0
    for i in range(count):
        monte_carlo_sum += fridge_room(price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4)
    
    monte_carlo_average = monte_carlo_sum / count
    return monte_carlo_average

def fridge_room(price, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4):
    # Designate random value to define if the door is open or closed for each time interval
    door_open_chance_value = np.random.random(len(price))

    # Set up temperature array, filled with zeros, except the start condition, which is assumed to be 5
    T = np.zeros(len(price))
    T[0] = 5

    # Calculate if the door is open by applying the conditional to door_open_chance_value
    c_1 = np.where(door_open_chance_value < 0.1, 3e-5, 5e-7)

    # Constants
    T_rum = 20
    T_komp = -5
    Delta_t = 300

    # Interesting result totals that need to be calculated
    total_power_cost = 0    
    total_food_waste = 0

    # Calculate each step of the way, what the temperature will be, without using i=0, as that is the starting condition
    for i in range(1, len(price)):
         c_2 = compressor_start(price, price[i], T[i-1], goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4)
         

         T[i] = T[i-1] + (c_1[i]*(T_rum - T[i-1]) + c_2*(T_komp - T[i-1]))*Delta_t
    
         # Calculate food waste based on last temperature. Since thats how much was lost because of that temperature until this time interval
         current_food_waste = 4.39*np.exp(-0.49*T[i-1]) if T[i-1] < 3.5 else (0.11*np.exp(0.31*T[i-1]) if T[i-1] > 6.5 else 0)
         total_food_waste += current_food_waste

         # Calculate power consumption based on if compressor was on
         total_power_cost += price[i] if c_2 > 0 else 0
    
    # Return the total cost
    return total_food_waste+total_power_cost

# Determine price intervals based on prices throughout September
avg_price = np.mean(price)
min_price = np.min(price)
max_price = np.max(price)
first_quartile = np.quantile(price, 0.25)
third_quartile = np.quantile(price, 0.75)



def compressor_start(price, current_price, current_temperature, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4):

        
        
    if min_price <= current_price < first_quartile:
        goal_temp = goal_temp_1
    elif first_quartile <= current_price < avg_price:
        goal_temp = goal_temp_2
    elif avg_price <= current_price < third_quartile:
        goal_temp = goal_temp_3
    elif third_quartile <= current_price <= max_price:
        goal_temp = goal_temp_4
    else:
        print("uh oh, something went VERY wrong")
        goal_temp = 1000  # just a fail safe number thats crazy high


    c_2 = 8e-6 if current_temperature > goal_temp else 0
    return c_2

main()