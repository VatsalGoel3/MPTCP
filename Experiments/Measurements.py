import subprocess
import csv
import time
import re

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode(), process.returncode

def main():
    try:
        # Record the start time
        start_time = time.time()

        # Prompt the user for the number of iterations
        num_iterations = int(input("Enter the number of iterations to run: "))
        cooldown_period = int(input("Enter the cooldown period in seconds between iterations: "))

        for iteration in range(num_iterations):
            # Run iperf3 command
            iperf_command = f"sudo mptcpize run ip netns exec h1 iperf3 -c 10.0.1.2 -t 10"
            iperf_output, iperf_error, iperf_returncode = run_command(iperf_command)

            print(f"\niperf3 iteration {iteration + 1} output:")
            print(iperf_output)
            print("iperf3 error:")
            print(iperf_error)

            # Extract average Bitrate from iperf3 output using regular expressions
            bitrate_match = re.search(r'(\d+\.\d+)\s+Mbits/sec\s+receiver', iperf_output)
            average_bitrate = float(bitrate_match.group(1)) if bitrate_match else None

            print(f"Average Bitrate: {average_bitrate} Mbits/sec")

            # Sleep for 2 seconds after iperf3
            time.sleep(2)

            # Run ping command
            ping_command = "sudo mptcpize run ip netns exec h1 ping -c 10 -i 1 10.0.1.2"
            ping_output, ping_error, ping_returncode = run_command(ping_command)

            print(f"\nPing iteration {iteration + 1} output:")
            print(ping_output)
            print("ping error:")
            print(ping_error)

            # Extract ping statistics (skip the first 2 lines)
            rtt_match = re.search(r'(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)\s+ms', ping_output)
            if rtt_match:
                rtt_min, rtt_avg, rtt_max, rtt_mdev = map(float, rtt_match.groups())
            else:
                rtt_min = rtt_avg = rtt_max = rtt_mdev = None

            print(f"RTT Min: {rtt_min} ms, RTT Avg: {rtt_avg} ms, RTT Max: {rtt_max} ms, RTT Mdev: {rtt_mdev} ms")

            # Log information in CSV file
            csv_file = "network_test_results.csv"
            with open(csv_file, mode='a') as file:
                writer = csv.writer(file)
                if iteration == 0:
                    writer.writerow(["Timestamp", "Average Bitrate (Mbits/sec)", "RTT Min (ms)", "RTT Avg (ms)", "RTT Max (ms)", "RTT Mdev (ms)"])
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), average_bitrate, rtt_min, rtt_avg, rtt_max, rtt_mdev])

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
