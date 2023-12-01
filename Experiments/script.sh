#!/bin/bash

# Default dataset files
dataset_file1="5G-Throughput-RTT-2023.csv"
dataset_file2="4G-Throughput-RTT-2023.csv"

# Fixed namespaces and interfaces
namespace1="r1"
interface1="eth3a"

namespace2="r2"
interface2="eth4a"

# Set the sleep duration and default iteration number
sleep_duration=0
iteration_number=0

while getopts "i:t:" opt; do
    case $opt in
        i)
            iteration_number="$OPTARG"
            ;;
        t)
            sleep_duration="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done

if [[ -z "$iteration_number" || -z "$sleep_duration" ]]; then
    echo "Usage: $0 -i <iteration_number> -t <sleep_duration>"
    exit 1
fi

configure_network_interface() {
    namespace=$1
    interface=$2
    download=$3
    upload=$4
    rtt=$5

    # Set the qdisc to 'root' to enable further editing
    ip netns exec "$namespace" tc qdisc replace dev "$interface" root netem delay "${rtt}ms" rate "${download}Mbit"

    # Print the imposed values
    echo "Imposing: "
    echo "Download: ${download} Mbit"
    echo "Upload: ${upload} Mbit"
    echo "RTT: ${rtt} ms"
    echo "on Network Interface $interface"
}

clear_network_configuration() {
    namespace=$1
    interface=$2

    # Clear any existing configuration on the network interface
    ip netns exec "$namespace" tc qdisc del dev "$interface" root
    echo "Cleared existing network configuration: Interface $interface."
}

main() {
    # Read the datasets
    dataset1=($(tail -n +2 "$dataset_file1"))
    dataset2=($(tail -n +2 "$dataset_file2"))

    # Ensure the iteration number is within bounds
    if [ "$iteration_number" -lt 1 ] || [ "$iteration_number" -gt "${#dataset1[@]}" ]; then
        echo "Invalid iteration number. It should be between 1 and ${#dataset1[@]}."
        exit 1
    fi

    # Adjust for array indexing (start from 0)
    ((iteration_number--))

    download1=$(echo "${dataset1[iteration_number]}" | cut -d',' -f1)
    upload1=$(echo "${dataset1[iteration_number]}" | cut -d',' -f2)
    rtt1=$(echo "${dataset1[iteration_number]}" | cut -d',' -f3)

    # Clear existing network configuration for namespace1 and interface1
    clear_network_configuration "$namespace1" "$interface1"

    # Configure the network interface for namespace1 and interface1
    configure_network_interface "$namespace1" "$interface1" "$download1" "$upload1" "$rtt1"

    download2=$(echo "${dataset2[iteration_number]}" | cut -d',' -f1)
    upload2=$(echo "${dataset2[iteration_number]}" | cut -d',' -f2)
    rtt2=$(echo "${dataset2[iteration_number]}" | cut -d',' -f3)

    # Clear existing network configuration for namespace2 and interface2
    clear_network_configuration "$namespace2" "$interface2"

    # Configure the network interface for namespace2 and interface2
    configure_network_interface "$namespace2" "$interface2" "$download2" "$upload2" "$rtt2"

    # Sleep for the specified duration between iterations
    sleep "$sleep_duration"
}

# Execute the main function
main
