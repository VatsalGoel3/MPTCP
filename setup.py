#!/usr/bin/env python3
import subprocess
import fileinput
import os

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return 0, result.stdout
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stderr

def update_upgrade_install_dkms():
    # Update, upgrade, and install dkms for Ubuntu 22.04
    print("Running: sudo apt update")
    run_command(["sudo", "apt", "update"])

    print("Running: sudo apt upgrade")
    run_command(["sudo", "apt", "upgrade", "-y"])

    print("Running: sudo apt install dkms -y --allow-change-held-packages")
    run_command(["sudo", "apt", "install", "dkms", "-y", "--allow-change-held-packages"])

def update_release_upgrades_file():
    # Open the file for in-place editing
    with fileinput.FileInput("/etc/update-manager/release-upgrades", inplace=True, backup=".bak") as file:
        for line in file:
            # Replace Prompt=lts with Prompt=normal
            print(line.replace("Prompt=lts", "Prompt=normal"), end="")

def check_and_upgrade_to_latest():
    # Run the release upgrade non-interactively
    print("Running: sudo do-release-upgrade -f DistUpgradeViewNonInteractive")
    run_command(["sudo", "do-release-upgrade", "-f", "DistUpgradeViewNonInteractive"])

def install_python_packages():
    # Install python3-pip, pandas, and scipy
    print("Running: sudo apt update")
    run_command(["sudo", "apt", "update"])

    print("Running: sudo apt upgrade")
    run_command(["sudo", "apt", "upgrade", "-y"])

    print("Running: sudo apt install python3-pip")
    run_command(["sudo", "apt", "install", "python3-pip", "-y"])

    print("Running: pip install pandas==1.4.4")
    run_command(["pip", "install", "pandas==1.4.4"])

    print("Running: pip install scipy==1.6.3")
    run_command(["pip", "install", "scipy==1.6.3"])

def clone_and_setup_errant():
    # Change directory to /users/VTG003
    print("Changing directory to /users/VTG003")
    os.chdir("/users/VTG003")

    # Clone the Errant repository
    print("Running: git clone https://github.com/marty90/errant.git")
    run_command(["git", "clone", "https://github.com/marty90/errant.git"])

    # Set up the path variable
    print("Setting up path variable")
    run_command(["export", "PATH=$PATH:/users/VTG003/errant"])

def reboot_system():
    print("Rebooting the system")
    run_command(["sudo", "reboot"])

def main():
    # Check Ubuntu version
    version_command = ["lsb_release", "-rs"]
    return_code, version_output = run_command(version_command)
    if return_code != 0:
        print(f"Error checking Ubuntu version:\n{version_output}")
        return

    ubuntu_version = version_output.strip()
    print(f"Detected Ubuntu version: {ubuntu_version}")

    if ubuntu_version == "22.04":
        # For Ubuntu 22.04, update, upgrade, and install dkms
        update_upgrade_install_dkms()

        # Continue with other tasks
        check_and_upgrade_to_latest()
        install_python_packages()
        clone_and_setup_errant()
    elif ubuntu_version == "20.04":
        # If Ubuntu version is 20.04, install required Python packages and set up Errant
        install_python_packages()
        clone_and_setup_errant()
    else:
        print("Unsupported Ubuntu version. Please upgrade to 20.04 or 22.04.")

    # Reboot the system after setup
    reboot_system()

if __name__ == "__main__":
    main()
