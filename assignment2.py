#!/usr/bin/env python3

# ======================================================
# OPS445 Assignment 2 - Group Project
# Author: Dhruv Thakar 154195226 dnthakar
# Part: Implemented interactive menu for firewall management:
#       1) Create new iptables rule
#       2) Apply all stored rules to the system
#       3) Flush all existing iptables rules
# ======================================================
#   My work in group project:
# - Built an interactive menu for testing and using firewall rules.
# - Added a feature to create new iptables rules by asking the user
#   for protocol, source IP, destination IP, and action (ACCEPT/DROP/REJECT).
# - If the user types “any” or leaves IP blank, I default it to 0.0.0.0/0.
# - Added a feature to apply all the rules to the system using `iptables`.
# - Added a feature to flush (clear) all current iptables rules from the system.
# - The program loops with a simple menu so we can keep creating, applying,
#   or flushing rules until we exit.
# ======================================================
# References:
# - iptables manual pages: https://linux.die.net/man/8/iptables
# - Python subprocess module: https://docs.python.org/3/library/subprocess.html
# - Python input() function: https://docs.python.org/3/library/functions.html#input
# ======================================================

import sys  # needed to exit the program
import subprocess  # needed to run system commands (iptables commands)

# I will keep the rules in a list for now. 
# Later, Purav will handle saving to JSON files.
rules_list = firewall_json.rules_list

def show_menu():
    """Just prints the simple menu for testing my part only."""
    print("\n==============================")
    print(" IPTables Frontend - Test Menu ")
    print("==============================")
    print("1. Create a new firewall rule")
    print("2. Apply all rules to the system")      
    print("3. Flush all iptables rules")            
    print("9. Exit program")

def create_rule():
    """
    Ask the user step-by-step for the details of a firewall rule.
    I kept it simple: protocol, source, destination, and action.
    """
    print("\n--- Create a New iptables Rule ---")

    # Step 1: Get protocol from the user
    protocol = input("Enter protocol (tcp/udp/icmp): ").strip().lower()
    if protocol not in ["tcp", "udp", "icmp"]:
        print("Sorry, that protocol is not supported. Try again.")
        return  # I return to the menu if the user made a mistake

    # Step 2: Get source IP
    source_ip = input("Enter source IP (or type 'any'): ").strip()
    # If the user says "any" or leaves it blank, we convert to 0.0.0.0/0 which means all IPs
    if source_ip == "" or source_ip.lower() == "any":
        source_ip = "0.0.0.0/0"

    # Step 3: Get destination IP
    dest_ip = input("Enter destination IP (or type 'any'): ").strip()
    if dest_ip == "" or dest_ip.lower() == "any":
        dest_ip = "0.0.0.0/0"

    # Step 4: Get action
    action = input("Enter action (ACCEPT/DROP/REJECT): ").strip().upper()
    if action not in ["ACCEPT", "DROP", "REJECT"]:
        print("Action must be ACCEPT, DROP, or REJECT. Returning to menu.")
        return

    # If all inputs are valid, I combine them into a rule string
    new_rule = f"-p {protocol} -s {source_ip} -d {dest_ip} -j {action}"

    # Add the rule to my temporary list
    rules_list.append(new_rule)

    print("\nRule created successfully!")
    print("Current rules entered by the user:")
    for index, rule in enumerate(rules_list, start=1):
        print(f"{index}. {rule}")

def apply_rules():
    """
    Applies all the stored firewall rules using iptables commands.
    Each rule string is used with 'iptables' to add it to the system.
    Requires root privileges.
    """
    if not rules_list:
        print("No rules to apply. Please create rules first.")
        return

    print("\nApplying all firewall rules to the system...")
    for rule in rules_list:
        cmd = f"sudo iptables -A INPUT {rule}"
        print(f"Running command: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Error: Failed to apply rule: {rule}")
            return
    print("All rules applied successfully!")

def flush_rules():
    """
    Flushes all iptables rules from the system.
    Also clears the local rules_list.
    Requires root privileges.
    """
    print("\nFlushing all iptables rules from the system...")
    try:
        subprocess.run("sudo iptables -F", shell=True, check=True)
        rules_list.clear()
        print("All iptables rules flushed successfully!")
    except subprocess.CalledProcessError:
        print("Error: Failed to flush iptables rules.")

# ---------------- MAIN LOOP ----------------
# I used a while loop so the menu keeps showing until the user exits.
while True:
    show_menu()
    choice = input("Choose an option: ").strip()

    if choice == "1":
        create_rule()
    elif choice == "2":               
        apply_rules()
    elif choice == "3":                
        flush_rules()
    elif choice == "9":
        print("Exiting the program. Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice, please try again.")
