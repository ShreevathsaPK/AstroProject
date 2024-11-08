import pandas as pd

# Define the Vimshottari Dasha system's planet years in the cycle (in years)
planetary_dasha_ratio = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

# Function to convert years to seconds
def years_to_seconds(years):
    return years * 365.25 * 24 * 60 * 60

def calculate_dasha_seq(planet_index,start_time, level_years, flag):
    
    res = []  # Initialize an empty list for storing the results

    # Convert dictionary items to a list for easy access by index
    planetary_dasha_items = list(planetary_dasha_ratio.items())

    # Set the starting index
    # Find the starting index based on the input planet
    
    start_index = planet_index  # For example, starting from 'Moon'

    # Iterate over the planetary dasha ratio dictionary
    for i in range(start_index, len(planetary_dasha_items) + start_index):
        planet, planet_ratio = planetary_dasha_items[i % len(planetary_dasha_items)]

        # Calculate the start and end times for this period
        end_time = start_time + planet_ratio * level_years / 120
        
        next_planet_index = next((i for i, (p, _) in enumerate(planetary_dasha_items) if p == planet), None)

        # Recursively calculate the sub-dasha for this planet
        if flag>1:
            sub_calulated_res = calculate_dasha_seq(next_planet_index,start_time, end_time-start_time, flag - 1)
            for sub_planet,sub_start_time,sub_end_time in sub_calulated_res:
                #res.append([planet+"->"+sub_planet, start_time, end_time,sub_calulated_res])
                res.append([planet+"->"+sub_planet, sub_start_time, sub_end_time])

        
        # Append the result with the current planet and its sub-period
        else:
            res.append([planet, start_time, end_time])
        
        # Update the start time for the next planet
        start_time = end_time

    return res

def main():
    
    result = calculate_dasha_seq(0, 0, 120, 5)  # Starting recursion
    print(result)
    return 0

if __name__ == "__main__":
    main()
