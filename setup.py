#!/usr/bin/env python3
import subprocess
import fileinput

def run_command(command):
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return 0, result.stdout
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stderr

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

def main():
    # Update package information
    print("Running: sudo apt update")
    run_command(["sudo", "apt", "update"])

    # Upgrade installed packages
    print("Running: sudo apt upgrade")
    return_code, upgrade_output = run_command(["sudo", "apt", "upgrade", "-y"])

    if return_code != 0:
        print(f"Error upgrading packages:\n{upgrade_output}")
    else:
        print("Upgrade successful.")

    # Update the release-upgrades file
    print("Updating /etc/update-manager/release-upgrades file")
    update_release_upgrades_file()

    # Check for any pending upgrades
    pending_upgrades = run_command(["apt", "list", "--upgradable"])

    if pending_upgrades:
        print("Pending upgrades:")
        print(pending_upgrades)
        print("Running: sudo apt upgrade for pending upgrades")
        return_code, upgrade_output = run_command(["sudo", "apt", "upgrade", "-y"])
        
        if return_code != 0:
            print(f"Error upgrading packages:\n{upgrade_output}")
        else:
            print("Upgrade successful.")

        # Update dkms after pending upgrades
        print("Running: sudo apt upgrade dkms")
        run_command(["sudo", "apt", "upgrade", "dkms"])

    # Check for a new release and upgrade
    check_and_upgrade_to_latest()

if __name__ == "__main__":
    main()
