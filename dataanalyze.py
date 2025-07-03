import pandas as pd

# Load the Fenerbahce player boxscores CSV
df = pd.read_csv('fenerbahce_player_boxscores.csv')

# Filter out rows where Player is 'TOTAL', 'TEAM', or is null/empty
df = df[df['Player'].notnull()]
df = df[~df['Player'].str.upper().isin(['TOTAL', 'TEAM'])]
df = df[df['Player'].str.strip() != '']

# Ensure 'Points' is numeric
df['Points'] = pd.to_numeric(df['Points'], errors='coerce')

# Find the row with the maximum points
max_points_row = df.loc[df['Points'].idxmax()]

print("Fenerbahce player with the highest points in a single match last season:")
print(f"Player: {max_points_row['Player']}")
print(f"GameID: {max_points_row['GameID']}")
print(f"Points: {max_points_row['Points']}")
print(f"Minutes: {max_points_row['Minutes']}")