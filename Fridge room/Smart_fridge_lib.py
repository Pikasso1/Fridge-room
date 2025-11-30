

def compressor_start(current_price, current_temperature, goal_temp_1, goal_temp_2, goal_temp_3, goal_temp_4, price_quantiles):
    """
    Input:
    current_price - Float
    current_temperature - Float
    goal_temp_1 - Float
    goal_temp_2 - Float
    goal_temp_3 - Float
    goal_temp_4 - Float
    price_quantiles - List of Floats

    Output:
    c_2 - Float

    Description: This function determines the c_2 value (compressor state) based on the current electricity price and temperature.

    # Test at lower price quartile, 2.5 given 1-5 quartile, and current temp above that intervals goal temp
    >>> compressor_start(2.5, 5.0, 4.0, 4.5, 5.0, 6.5, [1.0, 2.0, 3.0, 4.0, 5.0])
    8e-06
    """


    # Unpack price quantiles for readability
    min_price = price_quantiles[0]
    first_quartile = price_quantiles[1]
    avg_price = price_quantiles[2]
    third_quartile = price_quantiles[3]
    max_price = price_quantiles[4]
        
    # Apply the previously optimized goal temperatures for each quartile.
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


    # Turn on the compressor if the current temp is above the optimal cooling temp at current price
    c_2 = 8e-6 if current_temperature > goal_temp else 0
    return c_2

if __name__ == "__main__":
    import doctest
    doctest.testmod()