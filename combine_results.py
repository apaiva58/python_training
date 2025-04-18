import pandas as pd
import os
import re
from glob import glob

data_dir = "/Users/a.paivaaranda/Library/Mobile Documents/com~apple~CloudDocs/Documents/2021-01 python_training/games/"
main_file_path = os.path.join(data_dir, "main_file.csv")

def extract_date(filename):
    # Match "vrijdag", "zaterdag", or "zondag" followed by a date
    match = re.search(r'(vrijdag|zaterdag|zondag) (\d{1,2} \w+ \d{4})\.csv', filename, re.IGNORECASE)
    if match:
        date = match.group(2).strip()  # Extract only the date part

        # Map Dutch month abbreviations to English
        month_mapping = {
            "jan": "January",
            "feb": "February",
            "mrt": "March",
            "apr": "April",
            "mei": "May",
            "jun": "June",
            "jul": "July",
            "aug": "August",
            "sept": "September",
            "okt": "October",
            "nov": "November",
            "dec": "December"
        }

        # Replace Dutch month abbreviation with English
        for dutch, english in month_mapping.items():
            date = date.replace(dutch, english)

        return date
    return "Unknown Date"

def clean_uitslag_column(df):
    if "uitslag" in df.columns:
        # Clean up the "uitslag" column
        df["uitslag"] = df["uitslag"].astype(str).str.lstrip("'")
        
        # Add columns for home and away points
        def extract_points(uitslag, index):
            try:
                # Split the "Uitslag" into scores (e.g., "83 - 69" -> [83, 69])
                scores = list(map(int, uitslag.split("-")))  # Ensure scores are integers
                return scores[index]  # Return the score at the specified index
            except:
                return None  # Return None if parsing fails

        df["home_points"] = df["uitslag"].apply(lambda uitslag: extract_points(uitslag, 0))
        df["away_points"] = df["uitslag"].apply(lambda uitslag: extract_points(uitslag, 1))

        # Format the scores with a comma (European format)
        df["home_points"] = df["home_points"].apply(lambda x: f"{x}".replace(".", ",") if x is not None else None)
        df["away_points"] = df["away_points"].apply(lambda x: f"{x}".replace(".", ",") if x is not None else None)

        # Add a "Winner" column
        def determine_winner(uitslag):
            try:
                scores = list(map(int, uitslag.split("-")))  # Ensure scores are integers
                if scores[0] > scores[1]:
                    return "Home"
                elif scores[0] < scores[1]:
                    return "Away"
                else:
                    return "Draw"
            except:
                return "Unknown"

        df["winner"] = df["uitslag"].apply(determine_winner)
    return df

def process_file(file_path):
    try:
        df = pd.read_csv(
            file_path,
            sep=";",
            quotechar='"',
            encoding="utf-8",
            dtype=str
        )
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return pd.DataFrame()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Clean up uitslag and add winner column
    df = clean_uitslag_column(df)

    # Add date from filename
    date = extract_date(os.path.basename(file_path))
    print(f"Extracted date from {file_path}: {date}")  # Debugging
    df["datum"] = pd.to_datetime(date, format="%d %B %Y", errors="coerce")  # Convert to datetime

    return df

def update_main_file(new_files):
    dataframes = []

    if os.path.exists(main_file_path):
        existing_df = pd.read_csv(main_file_path, sep=";", quotechar='"', encoding="utf-8", dtype=str)
        dataframes.append(existing_df)

    for file in new_files:
        df = process_file(file)
        if not df.empty:
            dataframes.append(df)

    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)
        final_df.drop_duplicates(inplace=True)

        # Ensure 'datum' is consistently datetime
        final_df["datum"] = pd.to_datetime(final_df["datum"], errors="coerce")

        # Sort by date
        final_df.sort_values(by="datum", inplace=True)
        final_df.to_csv(main_file_path, sep=";", quotechar='"', index=False, encoding="utf-8")
        print(f"✅ main_file.csv updated: {len(final_df)} rows")
    else:
        print("⚠️ No valid data found in files.")

# Run the merge
new_files = glob(os.path.join(data_dir, "Gespeelde wedstrijden *.csv"))
update_main_file(new_files)
