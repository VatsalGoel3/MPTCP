import subprocess
import csv
import time

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode(), process.returncode

def configure_network(iteration):
    # Run the Bash script for network configuration
    bash_script_path = "./script.sh"
    bash_command = f"bash {bash_script_path} -i {iteration}"

    print(f"Running bash command: {bash_command}")

    # Run the Bash script for network configuration
    subprocess.run(bash_command, shell=True)

def extract_bitrate(iperf_output):
    lines = iperf_output.split('\n')
    for line in lines:
        if "receiver" in line:
            parts = line.split()
            if len(parts) >= 7:
                bitrate = parts[6]
                return float(bitrate) if bitrate.replace('.', '').isdigit() else None
    return None

def main():
    global num_iterations
    try:
        # Record the start time
        start_time = time.time()

        # Prompt the user for the number of iterations
        num_iterations = int(input("Enter the number of iterations to run: "))
        cooldown_period = int(input("Enter the cooldown period in seconds between iterations: "))

        for iteration in range(1, num_iterations + 1):
            # Running bash script to impose network conditions
            configure_network(iteration)

            time.sleep(2)

            # Run iperf3 command
            iperf_command = "sudo mptcpize run ip netns exec h1 iperf3 -c 10.0.1.2 -t 10"
            iperf_output, iperf_error, iperf_returncode = run_command(iperf_command)

            print(f"\niperf3 iteration {iteration} output:")
            print(iperf_output)
            print("iperf3 error:")
            print(iperf_error)

            # Extract average Bitrate from iperf3 output
            average_bitrate = extract_bitrate(iperf_output)

            if average_bitrate is not None:
                print(f"Average Bitrate: {average_bitrate} Mbits/sec")
            else:
                print("Error: Unable to extract Average Bitrate.")

            # Log information in CSV file
            csv_file = "network_test_results.csv"
            with open(csv_file, mode='a') as file:
                writer = csv.writer(file)
                if iteration == 1:
                    writer.writerow(["Timestamp", "Average Bitrate (Mbits/sec)"])
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), average_bitrate])

            # Sleep for the cooldown period
            time.sleep(cooldown_period)

        # Record the end time
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\nTotal execution time: {total_time} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
