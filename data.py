import csv

# Get input and output file names from the user
input_file_path = input("Enter the input file name (including extension, e.g., input.txt): ")
output_file_path = input("Enter the output file name (including extension, e.g., output.csv): ")

# Read data from the text file
with open(input_file_path, 'r') as txt_file:
    lines = txt_file.readlines()

# Extract relevant information and write to CSV
with open(output_file_path, 'w', newline='') as csv_file:
    # Define CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Write header
    csv_writer.writerow(['download', 'upload', 'rtt', 'operator'])
    
    # Process each line of the text file
    for line in lines:
        # Split the line into values
        values = line.strip().split(',')
        
        # Extract relevant information
        download_speed = float(values[5])
        upload_speed = float(values[6])
        rtt = float(values[7])
        operator = values[1]
        
        # Write the values to the CSV file
        csv_writer.writerow([download_speed, upload_speed, rtt, operator])

print(f"Conversion completed. Data has been written to {output_file_path}.")
