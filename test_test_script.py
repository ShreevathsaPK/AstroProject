# test_test_script.py
import subprocess

def test_process_inputs():
    # Simulate the input '1\nMars\n7\nAries\n' for the program.
    input_data = "1\nMars\n7\nAries\n"
    
    # Run the script using subprocess and feed inputs
    result = subprocess.run(
        ["python3", "\script_to_gen_horoscope_and_stor\query_script.py"],  # Adjust this if your script is in a different location
        input=input_data,              # Feeding the inputs
        text=True,                     # Treat input and output as text
        capture_output=True            # Capture the output
    )
    
    # Expected output
    expected_output = '''Query 1: Results for Mars in house 7
Vedartham Bharath
Charitha
Nandeesh
Bhargava K Bhat
Divya Bhat
Shreelakshmi Sangam Cousin
Kaushal Friend Sec
Pk Holla Dad
Pk Holla Dad
Goutham Kaushal Friend
Soumyashree K Holla
Medha Tent
Vedartham_Bharath
Vivek Trambadita
Manasa Ms Identified Scorpio asc bymyself
Shreya P B
Vedartham Bharath
Charitha
Nandeesh
Bhargava K Bhat
Divya Bhat
Sanketh Thotadur Holla
Shreelakshmi Sangam Cousin
Kaushal Friend Sec
Pk Holla Dad
Pk Holla Dad
Goutham Kaushal Friend
Soumyashree K Holla
Medha Tent
Vedartham_Bharath
Vivek Trambadita
Manasa Ms Identified Scorpio asc bymyself
Shreya P B
Query 1: Results for Mars in zodiac Aries
Shwetha B S
Suhana Mbrdi
Charitha
Prajnashri Achar
Vikas Soni
Suraj Thanush Freind
Chirag Aditya
Vinitha V
Vivek Trambadita
M Anjana Bhat
Shwetha B S
Suhana Mbrdi
Charitha
Prajnashri Achar
Vikas Soni
Suraj Thanush Freind
Chirag Aditya
Niveditha Nitin Friend
Vinitha V
Vivek Trambadita
M Anjana Bhat'''
    
    # Assert that the output is correct
    assert result.stdout.strip() == 34
