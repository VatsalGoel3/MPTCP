import subprocess
import pandas as pd
import time

def configure_network_interface(namespace, interface, download, upload, rtt):
    try:
        # Set the qdisc to 'root' to enable further editing
        subprocess.run(['ip', 'netns', 'exec', namespace, 'tc', 'qdisc', 'replace', 'dev', interface, 'root', 'netem'])

        # Set the data rate and delay on the network interface
        subprocess.run(['ip', 'netns', 'exec', namespace, 'tc', 'qdisc', 'add', 'dev', interface, 'root', 'netem', f'delay {rtt}ms rate {download}kbit'])

        # Print the imposed values
        print("Imposing values: ")
        print(f"{download} kbit download speed")
        print(f"{upload} kbit upload speed")
        print(f"{rtt} ms RTT on the network.")

    except subprocess.CalledProcessError as e:
        print(f"Error configuring network interface: {e}")

def clear_network_configuration(namespace, interface):
    try:
        # Clear any existing configuration on the network interface
        subprocess.run(['ip', 'netns', 'exec', namespace, 'tc', 'qdisc', 'del', 'dev', interface, 'root'])
        print("Cleared existing network configuration.")

    except subprocess.CalledProcessError as e:
        print(f"Error clearing network configuration: {e}")

def main():
    try:
        # Ask the user for the interface name, namespace name, and dataset file name
        namespace = input("Enter the namespace name (enter 'none' to skip using namespace): ").strip().lower()
        interface = input("Enter the interface name: ")
        dataset_file = input("Enter the dataset file name: ")

        # Read the dataset
        dataset = pd.read_csv(dataset_file)

        # Check if the user entered 'none' for the namespace
        if namespace == 'none':
            namespace = None

        # Iterate through the specified number of iterations
        num_iterations = int(input("Enter the number of iterations: "))
        sleep_duration = int(input("Enter the sleep duration between iterations in seconds: "))

        for iteration in range(num_iterations):
            download = dataset.iloc[iteration % len(dataset)]['download']
            upload = dataset.iloc[iteration % len(dataset)]['upload']
            rtt = dataset.iloc[iteration % len(dataset)]['rtt']

            # Clear existing network configuration if namespace is provided
            clear_network_configuration(namespace, interface)

            # Configure the network interface
            configure_network_interface(namespace, interface, download, upload, rtt)

            # Sleep for the specified duration between iterations
            time.sleep(sleep_duration)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
