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

def extract_ping_rtt(ping_output):
    try:
        rtt_line = ping_output.split('\n')[-2]
        rtt_parts = rtt_line.split('=')[-1].strip().split('/')
        rtt_min, rtt_avg, rtt_max, rtt_mdev = map(lambda x: float(x.split()[0]), rtt_parts)
        return rtt_min, rtt_avg, rtt_max, rtt_mdev
    except Exception as e:
        print(f"Error extracting ping RTT: {e}")
        return None, None, None, None

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

            # Run ping command
            ping_command = "sudo mptcpize run ip netns exec h1 ping -c 10 -i 1 10.0.1.2"
            ping_output, ping_error, ping_returncode = run_command(ping_command)

            print(f"\nPing iteration {iteration} output:")
            print(ping_output)
            print("ping error:")
            print(ping_error)

            # Extract ping statistics (skip the first 2 lines)
            rtt_min, rtt_avg, rtt_max, rtt_mdev = extract_ping_rtt(ping_output)

            if rtt_min is not None:
                print(f"RTT Min: {rtt_min} ms, RTT Avg: {rtt_avg} ms, RTT Max: {rtt_max} ms, RTT Mdev: {rtt_mdev} ms")
            else:
                print("Error: Unable to extract Ping RTT.")

            # Log information in CSV file
            csv_file = "network_test_results.csv"
            with open(csv_file, mode='a') as file:
                writer = csv.writer(file)
                if iteration == 1:
                    writer.writerow(["Timestamp", "RTT Min (ms)", "RTT Avg (ms)", "RTT Max (ms)", "RTT Mdev (ms)"])
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), rtt_min, rtt_avg, rtt_max, rtt_mdev])

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
