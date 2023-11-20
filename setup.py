#!/usr/bin/env python3
import subprocess
import fileinput

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None

def update_release_upgrades_file():
    # Open the file for in-place editing
    with fileinput.FileInput("/etc/update-manager/release-upgrades", inplace=True, backup=".bak") as file:
        for line in file:
            # Replace Prompt=lts with Prompt=normal
            print(line.replace("Prompt=lts", "Prompt=normal"), end="")

def main():
    # Update package information
    print("Running: sudo apt update")
    run_command(["sudo", "apt", "update"])

    # Upgrade installed packages
    print("Running: sudo apt upgrade")
    run_command(["sudo", "apt", "upgrade", "-y"])

    # Update the release-upgrades file
    print("Updating /etc/update-manager/release-upgrades file")
    update_release_upgrades_file()

    # Check for any pending upgrades
    pending_upgrades = run_command(["apt", "list", "--upgradable"])

    if pending_upgrades:
        print("Pending upgrades:")
        print(pending_upgrades)
        print("Running: sudo apt upgrade for pending upgrades")
        run_command(["sudo", "apt", "upgrade", "-y"])
    else:
        print("No pending upgrades.")

if __name__ == "__main__":
    main()
