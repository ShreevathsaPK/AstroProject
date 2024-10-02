import csv

def input_personal_info():
    personal_info = {}
    print("Enter Personal Information (press Enter after each entry):")
    personal_info['Name'] = input("Name: ")
    personal_info['Date'] = input("Date (DD/MM/YYYY): ")
    personal_info['Time'] = input("Time (HH:MM AM/PM): ")
    personal_info['Place'] = input("Place: ")
    personal_info['Latitude'] = input("Latitude: ")
    personal_info['Longitude'] = input("Longitude: ")
    personal_info['Timezone'] = input("Timezone: ")
    personal_info['Sunrise'] = input("Sunrise (HH:MM:SS): ")
    personal_info['Sunset'] = input("Sunset (HH:MM:SS): ")
    personal_info['Ayanamsha'] = input("Ayanamsha: ")
    personal_info['Comments'] = input("Comments: ")

    return personal_info

def input_planet_info():
    planet_data = []
    print("Enter Planet Information (type 'done' to finish):")
    
    while True:
        planet_info = {}
        planet_info['Planet'] = input("Planet: ")
        if planet_info['Planet'].lower() == 'done':
            break
        planet_info['Sign'] = input("Sign: ")
        planet_info['Sign Lord'] = input("Sign Lord: ")
        planet_info['Nakshatra'] = input("Nakshatra: ")
        planet_info['Naksh Lord'] = input("Naksh Lord: ")
        planet_info['Degree'] = input("Degree: ")
        planet_info['Retro(R)'] = input("Retro (Direct/Retro): ")
        planet_info['Combust'] = input("Combust (Yes/No): ")
        planet_info['Avastha'] = input("Avastha: ")
        planet_info['House'] = input("House: ")
        planet_info['Status'] = input("Status: ")
        
        planet_data.append(planet_info)

    return planet_data

def save_personal_info_to_csv(personal_info, filename='personal_info.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=personal_info.keys())
        writer.writeheader()
        writer.writerow(personal_info)

def save_planet_data_to_csv(planet_data, filename='planet_data.csv'):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['Planet', 'Sign', 'Sign Lord', 'Nakshatra', 'Naksh Lord', 'Degree', 'Retro(R)', 'Combust', 'Avastha', 'House', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for planet in planet_data:
            writer.writerow(planet)

def main():
    personal_info = input_personal_info()
    save_personal_info_to_csv(personal_info)

    planet_data = input_planet_info()
    save_planet_data_to_csv(planet_data)

    print("Data has been saved to 'personal_info.csv' and 'planet_data.csv'.")

if __name__ == "__main__":
    main()
