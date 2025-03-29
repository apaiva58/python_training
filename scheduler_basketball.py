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

# Fields and time slots
fields = ["Field 1", "Field 2", "Field 3", "Field 4"]  # Available fields
start_time = datetime(2025, 1, 20, 10, 0)  # Start time (8:00 AM)
end_time = datetime(2025, 1, 20, 20, 0)   # End time (8:00 PM)
time_slot_duration = 2  # Duration of each time slot in hours

# Priority categories for Field 1
priority_categories = ["M16-1", "M14-1", "MSE-1", "VSE-1"]

# Basket height requirements
youth_basket_categories = ["U10", "U12"]
adult_basket_categories = ["U14", "U16", "U18", "U22", "H1", "H2", "H3", "H4"]

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
    if category in youth_basket_categories:
        return "youth"
    elif category.split("-")[0] in adult_basket_categories:
        return "adult"
    return None

# Assign games to fields
for slot in slots:
    for field in fields:
        prioritized_games = [game for game in remaining_games if game["category"] in priority_categories]
        late_day_games = [game for game in remaining_games if any(cat in game["category"] for cat in late_day_categories)]
        other_games = [game for game in remaining_games if game not in prioritized_games + late_day_games]

        # Determine game pool for the current slot
        if slot.hour >= 16:  # Prioritize late-day categories in the evening
            game_pool = late_day_games + prioritized_games + other_games
        else:
            game_pool = prioritized_games + other_games

        for game in game_pool:
            required_height = get_required_basket_height(game["category"])
            current_height = field_basket_heights[field]["current"]

            # Check if the field can host the game
            if current_height is None or current_height == required_height or field_basket_heights[field]["changes"] < 1:
                # Assign game
                schedule.append({"time": slot, "field": field, "game_id": game["Nummer"], "category": game["category"]})
                remaining_games.remove(game)

                # Update field basket height
                if current_height != required_height:
                    field_basket_heights[field]["current"] = required_height
                    field_basket_heights[field]["changes"] += 1

                break

# Output the schedule
schedule_df = pd.DataFrame(schedule)
schedule_df = schedule_df.sort_values(by="time")  # Sort by time
print(schedule_df)
