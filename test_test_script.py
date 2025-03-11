# test_test_script.py
import subprocess

def test_process_inputs():
    # Simulate the input '1\nMars\n7\nAries\n' for the program.
    input_data = "1\nMars\n7\nAries\n"
    
    # Run the script using subprocess and feed inputs
    result = subprocess.run(
        ["python3", "test_script.py"],  # Adjust this if your script is in a different location
        input=input_data,              # Feeding the inputs
        text=True,                     # Treat input and output as text
        capture_output=True            # Capture the output
    )
    
    # Expected output
    expected_output = "Processed 1 Mars 7 Aries"
    
    # Assert that the output is correct
    assert result.stdout.strip() == expected_output
