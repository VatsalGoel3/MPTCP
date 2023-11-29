#!/bin/bash

# Default dataset file
dataset_file="Star.csv"

while getopts "n:d:i:t:" opt; do
    case $opt in
        n)
            namespace="$OPTARG"
            ;;
        d)
            interface="$OPTARG"
            ;;
        i)
            num_iterations="$OPTARG"
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

if [[ -z "$namespace" || -z "$interface" || -z "$num_iterations" || -z "$sleep_duration" ]]; then
    echo "Usage: $0 -n <namespace> -d <interface> -i <num_iterations> -t <sleep_duration>"
    exit 1
fi

configure_network_interface() {
    download=$1
    upload=$2
    rtt=$3

    # Set the qdisc to 'root' to enable further editing
    ip netns exec "$namespace" tc qdisc replace dev "$interface" root netem delay "${rtt}ms" rate "${download}kbit"

    # Print the imposed values
    echo "Imposing Metrics"
    echo "Download: ${download} kbit" 
    echo "Upload: ${upload} kbit" 
    echo "RTT: ${rtt} ms"
}

clear_network_configuration() {
    # Clear any existing configuration on the network interface
    ip netns exec "$namespace" tc qdisc del dev "$interface" root
    echo "Cleared existing network configuration."
}

main() {
    # Read the dataset
    dataset=($(tail -n +2 "$dataset_file"))

    for ((iteration = 0; iteration < num_iterations; iteration++)); do
        download=$(echo "${dataset[iteration % ${#dataset[@]}]}" | cut -d',' -f1)
        upload=$(echo "${dataset[iteration % ${#dataset[@]}]}" | cut -d',' -f2)
        rtt=$(echo "${dataset[iteration % ${#dataset[@]}]}" | cut -d',' -f3)

        # Clear existing network configuration if namespace is provided
        clear_network_configuration

        # Configure the network interface
        configure_network_interface "$download" "$upload" "$rtt"

        # Sleep for the specified duration between iterations
        sleep "$sleep_duration"
    done
}

# Execute the main function
main
