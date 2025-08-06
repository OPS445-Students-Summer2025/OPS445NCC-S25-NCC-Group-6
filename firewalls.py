#!/usr/bin/env python3

# ======================================================
# OPS445 Assignment 2 - Group Project
# Author: Purav Shah
# Part: JSON Save/Load Module for Firewalls
# ======================================================
# - Provides simple functions to save and load the rules_list
#   used by the main firewall script.
# - Saves rules in JSON format to preserve the firewall rules
#   created via create_rule().
# ======================================================
# References:
# - Python json module: https://docs.python.org/3/library/json.html
# - Python file I/O: https://docs.python.org/3/tutorial/inputoutput.html
# ======================================================

import json

# File where rules are saved/loaded
FILENAME = "firewall_rules.json"

# This will be overwritten by the main program's rules_list on import
rules_list = []

def save_rules():
    """Save the current rules_list to a JSON file."""
    try:
        with open(FILENAME, "w") as f:
            json.dump(rules_list, f, indent=2)
        print(f"The rules have been saved successfully to '{FILENAME}'.")
    except Exception as e:
        print("There has been an error in saving the rules:", e)

def load_rules():
    """Load rules from JSON file into rules_list."""
    global rules_list
    try:
        with open(FILENAME, "r") as f:
            rules_list = json.load(f)
        print(f"Rules loaded successfully from '{FILENAME}'.")
    except FileNotFoundError:
        print(f"No saved rules file was found ('{FILENAME}'). Creating new and starting fresh.")
        rules_list = []
    except Exception as e:
        print("There has been an error in loading the rules:", e)
