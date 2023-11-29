#!/bin/bash
set -e
exec > >(tee /var/log/setup.log) 2>&1

run_command() {
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo "Error: Command '$*' failed with exit code $status." >&2
        exit $status
    fi
}

update_upgrade_install_dkms() {
    # Update, upgrade, and install dkms for Ubuntu 22.04
    echo "Running: sudo apt update"
    run_command sudo apt update

    echo "Running: sudo apt upgrade"
    run_command sudo apt upgrade -y

    echo "Running: sudo apt install dkms -y --allow-change-held-packages"
    run_command sudo apt install dkms -y --allow-change-held-packages
}

update_release_upgrades_file() {
    # Replace Prompt=lts with Prompt=normal in /etc/update-manager/release-upgrades
    sudo sed -i.bak 's/Prompt=lts/Prompt=normal/' /etc/update-manager/release-upgrades
}

check_and_upgrade_to_latest() {
    # Run the release upgrade non-interactively
    echo "Running: sudo do-release-upgrade -f DistUpgradeViewNonInteractive"
    run_command sudo do-release-upgrade -f DistUpgradeViewNonInteractive
}

install_python_packages() {
    # Install python3-pip, pandas, and scipy
    echo "Running: sudo apt update"
    run_command sudo apt update

    echo "Running: sudo apt upgrade"
    run_command sudo apt upgrade -y

    echo "Running: sudo apt install python3-pip -y"
    run_command sudo apt install python3-pip -y

    echo "Running: pip install pandas==1.4.4"
    run_command pip install pandas==1.4.4

    echo "Running: pip install scipy==1.6.3"
    run_command pip install scipy==1.6.3
}

install_python_pandas() {
    # Install python3-pip, pandas, and scipy
    echo "Running: sudo apt update"
    run_command sudo apt update

    echo "Running: sudo apt upgrade"
    run_command sudo apt upgrade -y

    echo "Running: sudo apt install python3-pip -y"
    run_command sudo apt install python3-pip -y

    echo "Running: pandas install"
    run_command sudo apt install python3-pandas -y

}

clone_and_setup_errant() {
    # Change directory to /users/VTG003
    cd /users/VTG003 || exit

    # Clone the errant repository
    run_command git clone https://github.com/VatsalGoel3/errant.git

    # Set up the PATH variable
    errant_path="/users/VTG003/errant"
    export PATH=$PATH:$errant_path

    # Print the updated PATH for verification
    echo "Updated PATH: $PATH"
}

reboot_system() {
    echo "Rebooting the system"
    run_command sudo reboot
}

main() {
    # Check Ubuntu version
    ubuntu_version=$(lsb_release -rs)
    echo "Detected Ubuntu version: $ubuntu_version"

    if [ "$ubuntu_version" = "22.04" ]; then
        # For Ubuntu 22.04, update, upgrade, and install dkms
        update_upgrade_install_dkms
        # Update upgrade files
        update_release_upgrades_file
        # Upgrade to 23.04
        check_and_upgrade_to_latest
        #install pip and pandas
        install_python_pandas
    elif [ "$ubuntu_version" = "20.04" ]; then
        # If Ubuntu version is 20.04, install required Python packages and set up Errant
        install_python_packages
        clone_and_setup_errant
    else
        echo "Unsupported Ubuntu version. Please upgrade to 20.04 or 22.04."
        exit 1
    fi

    # Reboot the system after setup
    reboot_system
}

main
