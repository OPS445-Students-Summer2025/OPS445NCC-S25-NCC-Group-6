#!/usr/bin/env python3

# ======================================================
# OPS445 Assignment 2 - Group Project
# Final Combined Firewall Management Tool
# ======================================================
# Authors: 
#   - Dhruv Thakar: Rule creation, apply, and flush using iptables
#   - Purav Shah: Chain creation, view, delete, search, and edit
#   - Smeep Kaur: JSON save/load and TXT export/import with timestamps
# ======================================================
# Description:
#   This script combines all 3 team member modules into 
#   one unified firewall manager tool.
#
# Features:
#   1) Manage firewall rules interactively (create, apply, flush)
#   2) Create, view, delete, and edit iptables chains
#   3) Save/load rules and chains to JSON for persistence
#   4) Export/import rules to TXT for backup and sharing
#
# References:
#   - iptables manual: https://linux.die.net/man/8/iptables
#   - Python subprocess: https://docs.python.org/3/library/subprocess.html
#   - Python json: https://docs.python.org/3/library/json.html
#   - OPS445 Labs 1–8: https://seneca-ictoer.github.io/OPS445/
# ======================================================

import sys
import subprocess
import json
import datetime
import os

# ---------------- GLOBAL DATA ----------------
# rules_list: Stores all individual firewall rules (strings)
# chains: Stores named chains and their rules (dict of lists)
rules_list = []       
chains = {}           

# Files for persistence
RULES_JSON = "firewall_rules.json"
RULES_TXT = "firewall_rules.txt"

# ======================================================
#                DHURV'S MODULE
# Rule Management: Create, Apply, Flush
# ======================================================

def show_rule_menu():
    """Display Dhruv's submenu for managing basic rules"""
    print("\n=== Dhruv's Rule Menu ===")
    print("1. Create a new firewall rule")
    print("2. Apply all rules to the system")
    print("3. Flush all iptables rules")
    print("9. Back to main menu")

def create_rule():
    """
    Prompts user for protocol, source IP, destination IP, and action.
    Creates an iptables-compatible rule string and stores it in rules_list.
    """
    print("\n--- Create a New iptables Rule ---")
    protocol = input("Enter protocol (tcp/udp/icmp): ").strip().lower()
    if protocol not in ["tcp", "udp", "icmp"]:
        print("Invalid protocol.")
        return

    # Source IP (supports 'any')
    source_ip = input("Enter source IP (or 'any'): ").strip() or "any"
    if source_ip.lower() == "any":
        source_ip = "0.0.0.0/0"

    # Destination IP (supports 'any')
    dest_ip = input("Enter destination IP (or 'any'): ").strip() or "any"
    if dest_ip.lower() == "any":
        dest_ip = "0.0.0.0/0"

    # Action must be ACCEPT, DROP, or REJECT
    action = input("Enter action (ACCEPT/DROP/REJECT): ").strip().upper()
    if action not in ["ACCEPT", "DROP", "REJECT"]:
        print("Invalid action.")
        return

    # Combine into final rule string
    new_rule = f"-p {protocol} -s {source_ip} -d {dest_ip} -j {action}"
    rules_list.append(new_rule)
    print(f"[INFO] Rule added: {new_rule}")

def apply_rules():
    """
    Applies all rules in rules_list to the system using iptables.
    Uses subprocess to execute 'iptables -A INPUT <rule>'.
    """
    if not rules_list:
        print("No rules to apply.")
        return
    print("Applying all rules...")
    for rule in rules_list:
        cmd = f"sudo iptables -A INPUT {rule}"
        print(f"Running: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to apply rule: {rule}")

def flush_rules():
    """
    Flushes all iptables rules from the system and clears local list.
    """
    print("Flushing all iptables rules...")
    try:
        subprocess.run("sudo iptables -F", shell=True, check=True)
        rules_list.clear()
        print("All iptables rules flushed successfully!")
    except subprocess.CalledProcessError:
        print("Error flushing iptables rules.")

# ======================================================
#                PURAV'S MODULE
# Chain Management: Create, View, Delete, Search, Edit
# ======================================================

def show_chain_menu():
    """Displays Purav's chain management submenu"""
    print("\n=== Purav's Chain Menu ===")
    print("1. Create Chain")
    print("2. View Chains")
    print("3. Delete Chain")
    print("4. Search Chains")
    print("5. Edit Chain")
    print("9. Back to main menu")

def create_chain():
    """Creates a new named chain (stores as a key in chains dict)"""
    name = input("Enter new chain name: ").strip()
    if name in chains:
        print("Chain already exists.")
    else:
        chains[name] = []
        print("Chain created successfully.")

def view_chains():
    """Displays all chains and their rules"""
    if not chains:
        print("No chains available.")
    for chain, rules in chains.items():
        print(f"\nChain: {chain}")
        if rules:
            for i, r in enumerate(rules, start=1):
                print(f" {i}. {r}")
        else:
            print(" No rules.")

def delete_chain():
    """Deletes a chain by name"""
    name = input("Enter chain name to delete: ").strip()
    if name in chains:
        del chains[name]
        print("Chain deleted.")
    else:
        print("Chain not found.")

def search_chains():
    """Searches chain names for a keyword"""
    word = input("Enter keyword to search: ").strip()
    found = [name for name in chains if word in name]
    if found:
        for f in found:
            print("Found:", f)
    else:
        print("No matching chains.")

def edit_chain():
    """
    Allows user to view, add, and delete rules within a specific chain.
    """
    name = input("Enter chain to edit: ").strip()
    if name not in chains:
        print("Chain not found.")
        return
    while True:
        print(f"\nEditing chain: {name}")
        print("1. View rules")
        print("2. Add rule")
        print("3. Delete rule")
        print("4. Back")
        choice = input("Choose: ")
        if choice == "1":
            for i, r in enumerate(chains[name], start=1):
                print(f" {i}. {r}")
        elif choice == "2":
            rule = input("Enter rule: ")
            chains[name].append(rule)
            print("Rule added.")
        elif choice == "3":
            for i, r in enumerate(chains[name], start=1):
                print(f" {i}. {r}")
            num = input("Enter rule number to delete: ")
            if num.isdigit() and 1 <= int(num) <= len(chains[name]):
                del chains[name][int(num)-1]
                print("Rule deleted.")
            else:
                print("Invalid number.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

# ======================================================
#                SMEEP'S MODULE
# JSON Save/Load + TXT Export/Import with Timestamps
# ======================================================

def save_rules_json():
    """Saves all rules and chains to a JSON file for persistence."""
    data = {
        "rules": rules_list,
        "chains": chains
    }
    with open(RULES_JSON, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[INFO] Rules and chains saved to {RULES_JSON}")

def load_rules_json():
    """Loads rules and chains from a JSON file if available."""
    global rules_list, chains
    if not os.path.exists(RULES_JSON):
        print("[INFO] No JSON file found.")
        return
    with open(RULES_JSON, "r") as f:
        data = json.load(f)
        rules_list = data.get("rules", [])
        chains = data.get("chains", {})
    print(f"[INFO] Loaded {len(rules_list)} rules and {len(chains)} chains from JSON.")

def export_rules_txt():
    """
    Exports all current rules to a TXT file, 
    appending a timestamp for tracking.
    """
    with open(RULES_TXT, "w") as f:
        timestamp = datetime.datetime.now()
        for r in rules_list:
            f.write(f"{r}  # Exported {timestamp}\n")
    print(f"[INFO] Rules exported to {RULES_TXT}")

def import_rules_txt():
    """
    Imports rules from TXT backup into current rules_list.
    Avoids duplicates by checking existing rules.
    """
    if not os.path.exists(RULES_TXT):
        print("[INFO] No TXT file found to import.")
        return
    with open(RULES_TXT, "r") as f:
        for line in f:
            if line.strip():
                rule = line.split("#")[0].strip()
                if rule not in rules_list:
                    rules_list.append(rule)
    print(f"[INFO] Imported rules from {RULES_TXT}")

# ======================================================
#                MAIN MENU
# Combines all submenus and modules
# ======================================================

def main_menu():
    """Displays the main menu for the final combined script."""
    while True:
        print("\n=== Main Firewall Menu ===")
        print("1. Dhruv's Rule Menu")
        print("2. Purav's Chain Menu")
        print("3. Save to JSON")
        print("4. Load from JSON")
        print("5. Export to TXT")
        print("6. Import from TXT")
        print("9. Exit")
        choice = input("Choose: ").strip()
        
        # Dhruv's submenu
        if choice == "1":
            while True:
                show_rule_menu()
                c = input("Choose: ")
                if c == "1": create_rule()
                elif c == "2": apply_rules()
                elif c == "3": flush_rules()
                elif c == "9": break
        
        # Purav's submenu
        elif choice == "2":
            while True:
                show_chain_menu()
                c = input("Choose: ")
                if c == "1": create_chain()
                elif c == "2": view_chains()
                elif c == "3": delete_chain()
                elif c == "4": search_chains()
                elif c == "5": edit_chain()
                elif c == "9": break
        
        # Smeep's save/load/export/import
        elif choice == "3": save_rules_json()
        elif choice == "4": load_rules_json()
        elif choice == "5": export_rules_txt()
        elif choice == "6": import_rules_txt()
        
        elif choice == "9":
            print("Exiting Firewall Manager. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, try again.")

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    main_menu()
