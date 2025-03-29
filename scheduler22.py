import pandas as pd
from datetime import datetime, timedelta

# Load game data from CSV file
games_file = '/Users/antonio_paiva/Desktop/games_basis.csv'
games_df = pd.read_csv(games_file)

# Extract the category from 'Thuisteam'
def extract_category(team_name):
    return team_name.split()[-1]  # Assumes category is the last part of the team name

games_df['category'] = games_df['Thuisteam'].apply(extract_category)
games = games_df.to_dict('records')

# Get user input for schedule parameters
start_time_input = input("Enter the start time (e.g., 08:00): ")
end_time_input = input("Enter the end time (e.g., 20:00): ")
num_fields = int(input("Enter the number of fields available: "))

start_time = datetime(2025, 1, 20, int(start_time_input.split(':')[0]), int(start_time_input.split(':')[1]))
end_time = datetime(2025, 1, 20, int(end_time_input.split(':')[0]), int(end_time_input.split(':')[1]))

# Generate fields based on user input
fields = [f"Field {i+1}" for i in range(num_fields)]

time_slot_duration = 2  # Duration of each time slot in hours

# Priority categories for Field 1
priority_categories = ["M16-1", "M14-1", "MSE-1", "VSE-1"]

# Generate time slots
slots = []
time = start_time
while time + timedelta(hours=time_slot_duration) <= end_time:
    slots.append(time)
    time += timedelta(hours=time_slot_duration)

# Initialize schedule
schedule = []
remaining_games = games.copy()

# Track current basket height and changes for each field
field_basket_heights = {field: {"current": None, "changes": 0} for field in fields}

# Helper function to get required basket height
def get_required_basket_height(category):
    if "10" in category or "12" in category:  # Youth basket check
        return "youth"
    return "adult"

# Assign games to fields
for slot in slots:
    field_usage = {field: False for field in fields}  # Track field usage in the current slot

    # Check if any youth games remain
    youth_games_remaining = any(get_required_basket_height(game['category']) == "youth" for game in remaining_games)

    # First, assign priority games to Field 1 if possible
    for game in remaining_games[:]:
        if game["category"] in priority_categories and not field_usage["Field 1"]:
            required_height = get_required_basket_height(game["category"])

            # Check if Field 1 is compatible
            if (field_basket_heights["Field 1"]["current"] is None or
                field_basket_heights["Field 1"]["current"] == required_height or
                field_basket_heights["Field 1"]["changes"] < 1):

                # Assign the game to Field 1
                schedule.append({"time": slot, "field": "Field 1", "game_id": game["Nummer"], "category": game["category"]})
                remaining_games.remove(game)
                field_usage["Field 1"] = True

                # Update Field 1 basket height
                current_height = field_basket_heights["Field 1"]["current"]
                if current_height != required_height:
                    field_basket_heights["Field 1"]["current"] = required_height
                    field_basket_heights["Field 1"]["changes"] += 1

    # Then, assign remaining games to other fields
    for game in remaining_games[:]:
        required_height = get_required_basket_height(game["category"])

        # Find the first available field that matches the basket height
        field = next((f for f in fields if not field_usage[f] and (
            field_basket_heights[f]["current"] is None or
            field_basket_heights[f]["current"] == required_height or
            (field_basket_heights[f]["changes"] < 1 and not youth_games_remaining))), None)

        if field:
            # Assign the game to the field and time slot
            schedule.append({"time": slot, "field": field, "game_id": game["Nummer"], "category": game["category"]})
            remaining_games.remove(game)
            field_usage[field] = True

            # Update field basket height
            current_height = field_basket_heights[field]["current"]
            if current_height != required_height:
                field_basket_heights[field]["current"] = required_height
                field_basket_heights[field]["changes"] += 1

    # After assigning games in the current slot, refit youth fields if no youth games remain
    if not youth_games_remaining:
        for field, info in field_basket_heights.items():
            if info["current"] == "youth":
                info["current"] = "adult"  # Refit to adult

# Output the schedule
schedule_df = pd.DataFrame(schedule)
schedule_df = schedule_df.sort_values(by=["time", "field"])  # Sort by time and field
print(schedule_df)
