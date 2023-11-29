import subprocess
import pandas as pd
import time

def configure_network_interface(namespace, interface, download, upload, rtt):
    if namespace:
        # Set the data rate and delay on the network interface
        subprocess.run(['ip', 'netns', 'exec', namespace, 'tc', 'qdisc', 'add', 'dev', interface, 'root', 'netem', f'delay {rtt} rate {download}kbit'])

        # Print the imposed values
        print(f"Imposing {download} kbit download speed, {upload} kbit upload speed, and {rtt} ms RTT on the network.")

def clear_network_configuration(namespace, interface):
    if namespace:
        # Clear any existing configuration on the network interface
        subprocess.run(['ip', 'netns', 'exec', namespace, 'tc', 'qdisc', 'del', 'dev', interface, 'root'])

def main():
    # Ask the user for the interface name, namespace name, and dataset file name
    interface = input("Enter the interface name: ")
    namespace = input("Enter the namespace name (enter 'none' to skip using namespace): ").strip().lower()
    dataset_file = input("Enter the dataset file name: ")

    # Read the dataset
    dataset = pd.read_csv(dataset_file)

    # Check if the user entered 'none' for the namespace
    if namespace == 'none':
        namespace = None

    # Iterate through the specified number of iterations
    num_iterations = int(input("Enter the number of iterations: "))
    for iteration in range(num_iterations):
        download = dataset.iloc[iteration % len(dataset)]['download']
        upload = dataset.iloc[iteration % len(dataset)]['upload']
        rtt = dataset.iloc[iteration % len(dataset)]['rtt']

        # Clear existing network configuration if namespace is provided
        clear_network_configuration(namespace, interface)

        # Configure the network interface
        configure_network_interface(namespace, interface, download, upload, rtt)

        # Sleep for the specified duration between iterations
        time.sleep(int(input("Enter the sleep duration between iterations in seconds: ")))

if __name__ == "__main__":
    main()
