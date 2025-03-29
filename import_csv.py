import csv
import tkinter as tk
from tkinter import filedialog

# Open file dialog
root = tk.Tk()
root.withdraw()  # Hide the root window
input_file = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

if input_file:
    output_file = input_file.rsplit(".", 1)[0] + ".tsv"  # Change extension to .tsv

    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile, delimiter="\t")

        next(reader)  # Skip the first line

        for row in reader:
            row = [col.lstrip("#") for col in row]  # Strip # symbol

            # Convert quoted numbers to float-like format (keeping comma as decimal separator)
            if row[1].startswith('"') and row[1].endswith('"'):
                row[1] = row[1].strip('"')  # Remove quotes, keep comma

            writer.writerow(row)

    print(f"Processed file saved as: {output_file}")
else:
    print("No file selected.")
