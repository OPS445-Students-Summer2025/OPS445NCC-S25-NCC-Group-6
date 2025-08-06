#!/usr/bin/env python3

# ======================================================
# OPS445 Assignment 2 - Group Project
# Author: Purav Shah
# Part: Implemented interactive menu for iptables chain management:
#       1) Create, view, delete, and search rule chains
#       2) Add and delete individual rules inside chains
# ======================================================
# References:
# - Python range(): https://docs.python.org/3/library/functions.html#func-range
# - Python dictionaries: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
# - OPS445 Labs 1–8: https://seneca-ictoer.github.io/OPS445/
# ======================================================

chains = {}

# Creates a new chain and store it in the chains dictionary
def create_chain():
    name = input("Enter a new chain name: ")
    if name in chains:
        print("That chain already exists")
    else:
        chains[name] = []  # Creates a fresh empty list of rules
        print("The chain has been successfully created")

# Displaying all chains and their rules
def view_chains():
    if len(chains) == 0:
        print("No chains are available")
    else:
        for chain in chains:
            print("The chain:", chain)
            rules = chains[chain]
            if len(rules) == 0:
                print("There are no rules")
            else:
                for i in range(len(rules)): # Printing out all the rules in list[i] in ascending order
                    print(" ", i + 1, "-", rules[i])

# Allow user to delete a selected chain
def delete_chain():
    name = input("Enter a chain name to delete: ")
    if name in chains:
        del chains[name]
        print("The chain has been deleted")
    else:
        print("The chain has not been found")

# Allowing user to search chains by name using a keyword
def search_chains():
    word = input("Enter a search word: ")
    found = False
    for name in chains:
        if word in name:
            print("Found the search word:", name)
            found = True
    if found == False:
        print("There are no matching chains")

# Allow user to edit a specific chain which includes view, add, or delete rules
def edit_chain():
    name = input("Enter a chain name to edit: ")
    if name not in chains:
        print("Chain has not been found")
        return

    while True:
        print("\nWhat would you like to do?:", name)
        print("1. View rules")
        print("2. Add rule")
        print("3. Delete rule")
        print("4. Back")

        choice = input("Please enter a choice: ")

        if choice == "1":
            rules = chains[name]
            if len(rules) == 0:
                print(" No rules are available")
            else:
                for i in range(len(rules)):
                    print(" ", i + 1, "-", rules[i])

        elif choice == "2":
            rule = input("Enter a rule: ")
            chains[name].append(rule)
            print("Rule has been added successfully")

        elif choice == "3":
            rules = chains[name]
            if len(rules) == 0:
                print("  No rules have been found to delete.")
            else:
                for i in range(len(rules)):
                    print(" ", i + 1, "-", rules[i])
                num = input("Enter a rule number to delete: ")
                if num.isdigit():
                    n = int(num)
                    if n >= 1 and n <= len(rules):
                        del rules[n - 1]
                        print("Rule has been successfully deleted")
                    else:
                        print("Not a valid Number")
                else:
                    print("Please enter a number")

        elif choice == "4":
            break
        else:
            print("Not a valid option. Please try again")

# Main menu fuction
def menu():
    while True:
        print("\n=== Chain Storage ===")
        print("1. Create Chain")
        print("2. View Chains")
        print("3. Delete Chain")
        print("4. Search Chains")
        print("5. Edit Chain")
        print("6. Exit")

        choice = input("What option do you choose?: ")

        if choice == "1":
            create_chain()
        elif choice == "2":
            view_chains()
        elif choice == "3":
            delete_chain()
        elif choice == "4":
            search_chains()
        elif choice == "5":
            edit_chain()
        elif choice == "6":
            print("Thank you, Goodbye!")
            break
        else:
            print("Not a valid option. Please try again")

# Calling the program to start
menu()
