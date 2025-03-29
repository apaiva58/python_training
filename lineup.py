import csv
import tkinter as tk
from tkinter import messagebox, simpledialog

# Function to parse the player list from a TSV file


def parse_player_list(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip header
        # Assuming columns are in this order
        return [{"Nummer": int(row[0]), "Voornaam": row[1], "Naam": row[2]} for row in reader]

# Function to create the GUI for selecting players


def select_players_gui(player_list, num_players):
    root = tk.Tk()
    root.title("Select Players")

    selected_players = []
    selected_count = tk.IntVar(value=0)

    def update_checkboxes():
        count = selected_count.get()
        for var, checkbox in zip(vars, checkboxes):
            if not var.get() and count >= num_players:
                checkbox.config(state=tk.DISABLED)
            else:
                checkbox.config(state=tk.NORMAL)

    def on_check(var):
        if var.get():
            selected_count.set(selected_count.get() + 1)
        else:
            selected_count.set(selected_count.get() - 1)
        update_checkboxes()

    def submit():
        selected_players.clear()
        for idx, var in enumerate(vars):
            if var.get():
                selected_players.append(player_list[idx])
        if len(selected_players) != num_players:
            messagebox.showinfo("Info", f"Selected {len(selected_players)} players, but expected {
                                num_players}. Please select exactly {num_players} players.")
        else:
            root.destroy()

    tk.Label(root, text=f"Select {num_players} Players:").pack()

    vars = []
    checkboxes = []
    for player in player_list:
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(root, text=f"{player['Voornaam']} {
                                  player['Naam']}", variable=var, command=lambda v=var: on_check(v))
        checkbox.pack(anchor='w')
        vars.append(var)
        checkboxes.append(checkbox)

    tk.Button(root, text="Submit", command=submit).pack()

    root.mainloop()
    return selected_players

# Function to create a TSV file with the selected lineup


def create_tsv(players, output_path):
    # Sort players by 'Nummer' column
    sorted_players = sorted(players, key=lambda x: x["Nummer"])

    with open(output_path, "w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["Nummer", "Voornaam", "Naam"])  # Header
        for player in sorted_players:
         writer.writerow(
        [player["Nummer"], player["Voornaam"], player["Naam"]])
    print(f"\nLineup saved to {output_path}")


# Example usage
if __name__ == "__main__":
    file_path = "/Users/a.paivaaranda/Library/Mobile Documents/com~apple~CloudDocs/Documents/2021-01 python_training/pioneers163/Werkblad 5-Tabel 1-1-1.tsv"  # Input file path
    output_path = "/Users/a.paivaaranda/Library/Mobile Documents/com~apple~CloudDocs/Documents/2021-01 python_training/pioneers163/lineup.tsv"  # Output file path

    # Parse players from the input file
    player_list = parse_player_list(file_path)
    print(f"Loaded {len(player_list)} players.")

    # Get the number of players to select from user input
    num_players = simpledialog.askinteger("Input", f"Enter the number of players to select (1-{
                                          len(player_list)}):", minvalue=1, maxvalue=len(player_list))

    if num_players is None:
        messagebox.showinfo("Info", "No number of players entered. Exiting.")
        exit()

    # Select players using GUI
    selected_players = select_players_gui(player_list, num_players)

    if len(selected_players) != num_players:
        messagebox.showinfo("Info", f"Selected {len(
            selected_players)} players, but expected {num_players}. Exiting.")
        exit()

    # Print selected players
    print("\nSelected Players:")
    # Sort the selected players by 'Nummer'
    sorted_selected_players = sorted(
        selected_players, key=lambda x: x["Nummer"])
    for idx, player in enumerate(sorted_selected_players):
        print(f"{idx + 1}. {player['Nummer']
                            } {player['Voornaam']} {player['Naam']}")

    # Show selected players in a message box
    selected_players_str = "\n".join([f"{player['Nummer']} {player['Voornaam']} {
                                     player['Naam']}" for player in sorted_selected_players])
    messagebox.showinfo("Selected Players", f"Selected Players:\n{
                        selected_players_str}")

    # Create the lineup TSV file
    create_tsv(sorted_selected_players, output_path)
