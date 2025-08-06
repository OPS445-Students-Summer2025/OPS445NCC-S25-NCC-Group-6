#!/usr/bin/env python3

# ======================================================
# OPS445 Assignment 2 - Group Project
# Author: Smeep (Placeholder)
# Part: Firewall Rule Persistence and Export/Import
# ======================================================
# My responsibilities in this group project:
# 1) Save and load all firewall rules/chains to JSON.
# 2) Export rules to a human-readable text file for backup.
# 3) Import rules from a text file to restore previous state.
# 4) Add timestamps and optional comments when creating rules.
# 5) Provide a small standalone menu for testing this module
#    without running the full project.
# ======================================================
# References:
# - Python json module: https://docs.python.org/3/library/json.html
# - Python datetime module: https://docs.python.org/3/library/datetime.html
# - Python file I/O: https://docs.python.org/3/tutorial/inputoutput.html
# ======================================================

import json
import datetime
import os

# Default filenames for persistence
JSON_FILE = "firewall_rules.json"
EXPORT_FILE = "firewall_rules.txt"

# In the full project, this rules_list will be linked to Dhruv’s main menu
# Here, I initialize it so the module can work standalone.
rules_list = []

# ----------------- JSON Save/Load -----------------

def save_rules_to_json():
    """
    Save current rules_list to a JSON file.
    Each rule is stored as a dictionary with:
    - 'rule': the actual iptables string
    - 'comment': optional comment
    - 'timestamp': when it was created
    """
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(rules_list, f, indent=4)
        print(f"[INFO] Rules saved successfully to '{JSON_FILE}'.")
    except Exception as e:
        print(f"[ERROR] Failed to save rules to JSON: {e}")


def load_rules_from_json():
    """
    Load rules_list from JSON file if it exists.
    Returns an updated rules_list.
    """
    global rules_list
    try:
        with open(JSON_FILE, "r") as f:
            rules_list = json.load(f)
        print(f"[INFO] Loaded {len(rules_list)} rules from '{JSON_FILE}'.")
    except FileNotFoundError:
        print(f"[INFO] No JSON file found. Starting with an empty rule list.")
        rules_list = []
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON file is corrupted: {e}")
        rules_list = []
    return rules_list

# ----------------- Export/Import as Text -----------------

def export_rules_to_text():
    """
    Export all current rules to a human-readable text file.
    Format:
        <rule>  # Comment (Timestamp)
    """
    try:
        with open(EXPORT_FILE, "w") as f:
            for r in rules_list:
                rule = r.get("rule", "")
                comment = r.get("comment", "")
                timestamp = r.get("timestamp", "")
                line = f"{rule}"
                if comment or timestamp:
                    line += f"  # {comment} ({timestamp})"
                f.write(line + "\n")
        print(f"[INFO] Rules exported to '{EXPORT_FILE}'.")
    except Exception as e:
        print(f"[ERROR] Failed to export rules: {e}")


def import_rules_from_text():
    """
    Import rules from the human-readable text file.
    Assumes one rule per line, comments start with '#'.
    """
    global rules_list
    if not os.path.exists(EXPORT_FILE):
        print(f"[ERROR] No export file '{EXPORT_FILE}' found.")
        return

    try:
        with open(EXPORT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "#" in line:
                    rule_part, comment_part = line.split("#", 1)
                    rule = rule_part.strip()
                    comment = comment_part.strip()
                else:
                    rule = line
                    comment = "Imported rule"
                rules_list.append({
                    "rule": rule,
                    "comment": comment,
                    "timestamp": str(datetime.datetime.now())
                })
        print(f"[INFO] Imported rules from '{EXPORT_FILE}'.")
    except Exception as e:
        print(f"[ERROR] Failed to import rules: {e}")

# ----------------- Rule Creation with Timestamp -----------------

def create_rule():
    """
    Ask user to type a raw iptables rule string and optional comment.
    Adds a timestamp automatically.
    """
    rule = input("Enter a new firewall rule string (ex: -p tcp -s 0.0.0.0/0 -j ACCEPT): ").strip()
    if not rule:
        print("No rule entered. Returning to menu.")
        return

    comment = input("Enter an optional comment for this rule: ").strip()
    timestamp = str(datetime.datetime.now())

    rules_list.append({
        "rule": rule,
        "comment": comment,
        "timestamp": timestamp
    })
    print(f"[INFO] Rule added successfully at {timestamp}.")

# ----------------- Standalone Test Menu -----------------

def show_menu():
    print("\n==============================")
    print("  Smeep's Firewall Module Menu ")
    print("==============================")
    print("1. Create new rule with timestamp")
    print("2. View current rules")
    print("3. Save rules to JSON")
    print("4. Load rules from JSON")
    print("5. Export rules to text file")
    print("6. Import rules from text file")
    print("9. Exit")

def view_rules():
    if not rules_list:
        print("[INFO] No rules to display.")
        return
    print("\nCurrent Firewall Rules:")
    for idx, r in enumerate(rules_list, 1):
        print(f"{idx}. {r['rule']}  # {r['comment']} ({r['timestamp']})")

if __name__ == "__main__":
    load_rules_from_json()  # Load existing rules on startup
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_rule()
        elif choice == "2":
            view_rules()
        elif choice == "3":
            save_rules_to_json()
        elif choice == "4":
            load_rules_from_json()
        elif choice == "5":
            export_rules_to_text()
        elif choice == "6":
            import_rules_from_text()
        elif choice == "9":
            print("Exiting Smeep's module. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")