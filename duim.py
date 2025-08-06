#!/usr/bin/env python3
"""
OPS445 Assignment 2 - duim

Author: Festus Uwhumiakpo
Student ID: fouwhumiakpo
Email: fouwhumiakpo@myseneca.ca

Description:
This script is a Python-enhanced version of the 'du' command, providing
visual bar graphs for folder sizes and additional formatting options.

This file is the starting template. You will build your script function-by-function.
"""

import sys
import os
import argparse
import subprocess

# Step 1: percent_to_graph
def percent_to_graph(percent, total_chars=20, symbol="#"):
    """
    Returns a string bar graph based on the percent value.

    Example:
    >>> percent_to_graph(50)
    '##########----------'
    """
    try:
        percent = float(percent)
        filled_length = int(round(total_chars * percent / 100))
        empty_length = total_chars - filled_length
        return symbol * filled_length + '-' * empty_length
    except Exception as e:
        return f"ERROR: {e}"

# Placeholder for future steps
def main():
    pass

if __name__ == '__main__':
    main()

# Step 2: get_size
def get_size(path):
    """
    Recursively calculates total size (in KB) of the given file or directory.

    Returns:
        - Integer size in kilobytes
        - If error, returns string "ERROR: <error message>"
    """
    total_size = 0

    try:
        if os.path.isfile(path):
            # It's a file, return size in KB
            total_size = os.path.getsize(path) // 1024
        elif os.path.isdir(path):
            # It's a directory, walk through it
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    full_path = os.path.join(dirpath, f)
                    if os.path.isfile(full_path):
                        total_size += os.path.getsize(full_path) // 1024
        else:
            return "ERROR: Not a valid file or directory"
        return total_size
    except Exception as e:
        return f"ERROR: {e}"

# Step 3: build_filelist
def build_filelist(path):
    """
    Builds a list of (name, size) tuples for the given directory.
    Includes only immediate subdirectories and files in that directory.
    Uses get_size(path) to calculate size in KB.

    Returns:
        - List of tuples
        - If error, returns string "ERROR: <error message>"
    """
    filelist = []

    try:
        if not os.path.isdir(path):
            return "ERROR: Not a directory"

        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            size = get_size(full_path)
            filelist.append((entry, size))

        return filelist
    except Exception as e:
        return f"ERROR: {e}"

def format_filelist(data, maxname=20, graph=False):
    """
    Formats the list of (name, size) tuples into a printable string.

    Args:
        data: list of (name, size) tuples
        maxname: max width of the name column
        graph: if True, append visual graph to each line

    Returns:
        A formatted string
    """
    try:
        if not isinstance(data, list):
            return "ERROR: Invalid data"

        output = ""
        for name, size in data:
            # Truncate or pad the name
            display_name = name[:maxname].ljust(maxname)
            size_str = str(size).rjust(5) + " KB"

            if graph:
                percent = min(100, int(size))  # prevent crazy bars
                bar = percent_to_graph(percent)
                output += f"{display_name} | {size_str} | {bar}\n"
            else:
                output += f"{display_name} | {size_str}\n"

        return output.strip()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="duim: Disk usage with bar graphs"
    )
    parser.add_argument(
        "-p", "--path",
        required=True,
        help="Path to directory"
    )
    parser.add_argument(
        "-g", "--graph",
        action="store_true",
        help="Display bar graph"
    )
    parser.add_argument(
        "-m", "--maxname",
        type=int,
        default=20,
        help="Max name length"
    )

    args = parser.parse_args()

    filelist = build_filelist(args.path)
    output = format_filelist(filelist, maxname=args.maxname, graph=args.graph)
    print(output)
