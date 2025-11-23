import numpy as np

def main():
    price = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])
    result = fridge_room(price, 5)
    print(result)

def fridge_room(price, goal_temp):
    # Designate random value to define if the door is open or closed for each time interval
    np.random.seed(42)
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
         c_2 = 8e-6 if T[i-1] > goal_temp else 0
         

         T[i] = T[i-1] + (c_1[i]*(T_rum - T[i-1]) + c_2*(T_komp - T[i-1]))*Delta_t
    
         # Calculate food waste based on last temperature. Since thats how much was lost because of that temperature until this time interval
         current_food_waste = 4.39*np.exp(-0.49*T[i-1]) if T[i-1] < 3.5 else (0.11*np.exp(0.31*T[i-1]) if T[i-1] > 6.5 else 0)
         total_food_waste += current_food_waste

         # Calculate power consumption based on if compressor was on
         total_power_cost += price[i] if c_2 > 0 else 0
    
    # Return the total cost
    return total_food_waste+total_power_cost
#main()



def test():
    for i in range(100):
        pris = np.genfromtxt("elpris.csv", delimiter=",", usecols=[1])
        gennemsnits_pris = np.average(pris)
        højeste_pris = np.max(pris)
        laveste_pris = np.min(pris)

        1_kvadrant = (gennemsnits_pris - laveste_pris) / 2
        3_kvadrant = (højeste_pris - gennemsnits_pris) / 2

        nuværende_pris = pris[i]
        mål_temperatur = 0

        if laveste_pris <= nuværende_pris < 1_kvadrant:
            mål_temperatur = 3.5
        elif 1_kvadrant <= nuværende_pris < gennemsnits_pris:
            mål_temperatur = 4.5
        elif gennemsnits_pris <= nuværende_pris < 3_kvadrant:
            mål_temperatur = 5
        elif 3_kvadrant <= nuværende_pris <= højeste_pris:
            mål_temperatur = 6

test()




