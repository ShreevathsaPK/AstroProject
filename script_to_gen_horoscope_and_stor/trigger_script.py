import os
import subprocess
import pandas as pd

def process_excel_files(folder_path):
    # Define CSV filenames
    personal_info_csv = 'personal_info.csv'
    planet_info_csv = 'planet_data.csv'
    
    # Loop through all Excel files in the specified folder
    for filename in os.listdir(folder_path):
        print("***DEBUG**")
        if filename.endswith(('.xls', '.xlsx')):
            excel_file_path = os.path.join(folder_path, filename)
            print("Processing file: {}".format(excel_file_path))

            # Read personal info from the first sheet (row-wise format)
            personal_info_df = pd.read_excel(excel_file_path, sheet_name="Sheet 1", header=None)

            # Drop rows where all values are NaN and filter valid rows
            personal_info_df = personal_info_df.dropna(how='all')

            # Convert to a dictionary (assuming first column as key, second column as value)
            personal_info = dict(zip(personal_info_df[0], personal_info_df[1]))

            # Debug: Print the cleaned personal info
            print("Personal Info Read: ", personal_info)

            # Write personal info to CSV
            with open(personal_info_csv, 'w') as personal_file:
                # Write header
                personal_file.write("Name,Date,Time,Place,Latitude,Longitude,Timezone,Sunrise,Sunset,Ayanamsha,Comments\n")
                # Write personal info
                personal_file.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(
                    personal_info.get('Name', ''),
                    personal_info.get('Date', ''),
                    personal_info.get('Time', ''),
                    personal_info.get('Place', ''),
                    personal_info.get('Latitude', ''),
                    personal_info.get('Longitude', ''),
                    personal_info.get('Timezone', ''),
                    personal_info.get('Sunrise', ''),
                    personal_info.get('Sunset', ''),
                    personal_info.get('Ayanamsha', ''),
                    personal_info.get('Comments', '')
                ))
            print("Wrote personal info to {}".format(personal_info_csv))

            # Read planetary data from the second sheet
            planet_info_df = pd.read_excel(excel_file_path, sheet_name="Sheet 2" , header = 1)
            print(planet_info_df)
            # Check if the DataFrame is not empty and contains the expected columns
            if not planet_info_df.empty:
                if 'Planet' in planet_info_df.columns:
                    planet_info_df.to_csv(planet_info_csv, index=False, encoding='utf-8')
                    print("Wrote planetary data to {}".format(planet_info_csv))
                else:
                    print("Error: 'Planet' column not found in the data.")
            else:
                print("Planetary data is empty.")

            # Call the previous script to add data to the database
            subprocess.call(['python', 'dob_to_chart.py'])

if __name__ == "__main__":
    folder_path = 'dataset'  # Change this to your folder path
    process_excel_files(folder_path)
    print("****DONE****BINGO****")
