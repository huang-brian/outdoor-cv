# expands or abbreviates month names in a CSV file's 'date' field based on user input
# args --ex or --ab to specify mode
# example usage: python month_abr.py outdoorcv.csv --expand
import csv
import sys
import os
import calendar
import argparse

def process_months(input_file, mode):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Generate mapping based on the mode
    if mode == "expand":
        # Jan -> January
        month_map = {abbr: full for abbr, full in zip(calendar.month_abbr[1:], calendar.month_name[1:])}
        suffix = "_expanded"
    else:
        # January -> Jan
        month_map = {full: abbr for abbr, full in zip(calendar.month_abbr[1:], calendar.month_name[1:])}
        suffix = "_abbreviated"

    name, ext = os.path.splitext(input_file)
    output_file = f"{name}{suffix}{ext}"

    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    date_val = row['date']
                    parts = date_val.split()
                    
                    # Replace the month if it exists in our map
                    updated_parts = [month_map.get(part, part) for part in parts]
                    
                    row['date'] = " ".join(updated_parts)
                    writer.writerow(row)

        print(f"Success! {mode.capitalize()}ed file saved as: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expand or abbreviate month names in a CSV 'date' field.")
    parser.add_argument("input", help="Path to the input CSV file")
    
    group = parser.add_mutually_exclusive_group(required=True)
    # Added --ex and --ab as aliases
    group.add_argument("--expand", "--ex", action="store_true", help="Convert Jan to January")
    group.add_argument("--abbreviate", "--ab", action="store_true", help="Convert January to Jan")

    args = parser.parse_args()

    mode = "expand" if args.expand else "abbreviate"
    process_months(args.input, mode)