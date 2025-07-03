import pandas as pd
from euroleague_api.boxscore_data import BoxScoreData
import json
import time

season = 2023  # 2023-24 season
competition_code = "E"  # 'E' for EuroLeague
fener_codes = ['ULK']  # Fenerbahce's team code in the data

# --- To fetch the EuroLeague schedule from the API, uncomment and run this block ---
# from euroleague_api.game_metadata import GameMetadata
# games = GameMetadata(competition_code)
# schedule = games.get_game_metadata_single_season(season)
# schedule_df = pd.DataFrame(schedule)
# schedule_df.to_csv('euroleague_schedule.csv', index=False)
# print('EuroLeague schedule saved to euroleague_schedule.csv')

schedule_df = pd.read_csv('euroleague_schedule.csv')
schedule = schedule_df.to_dict(orient='records')

rows = []
for idx, game in enumerate(schedule):  # Process all games
    if isinstance(game, str):
        game = json.loads(game)
    # Try all possible game code keys
    game_code = (
        game.get('GameCode') or
        game.get('Gamecode') or
        game.get('gamecode') or
        game.get('game_code')
    )
    if not game_code:
        continue
    try:
        # Ensure game_code is int
        game_code_int = int(game_code)
        print(f"Processing game {idx+1}/{len(schedule)} (GameCode: {game_code_int})")
        result = BoxScoreData(competition_code).get_player_boxscore_stats_data(season, game_code_int)
        # Handle DataFrame result
        if isinstance(result, pd.DataFrame):
            # Normalize 'Team' column
            result['Team'] = result['Team'].astype(str).str.strip().str.upper()
            fener_df = result[result['Team'].isin([code.upper() for code in fener_codes])]
            for _, player in fener_df.iterrows():
                rows.append({
                    'GameID': game_code_int,
                    'Player': player.get('Player', player.get('PlayerName')),
                    'Minutes': player.get('Minutes', player.get('Min')),
                    'Points': player.get('Points', player.get('Pts')),
                    'IsStarter': player.get('IsStarter'),
                    'TotalRebounds': player.get('TotalRebounds'),
                    'Assistances': player.get('Assistances'),
                    'Valuation': player.get('Valuation'),
                    'Plusminus': player.get('Plusminus')
                })
        # Handle list-of-dict result
        elif isinstance(result, list):
            for player in result:
                if isinstance(player, str):
                    try:
                        player = json.loads(player)
                    except Exception:
                        continue
                if (isinstance(player, dict) and (
                    str(player.get('Team', '')).strip().upper() in [code.upper() for code in fener_codes] or
                    str(player.get('CodeTeam', '')).strip().upper() in [code.upper() for code in fener_codes] or
                    str(player.get('TVCode', '')).strip().upper() in [code.upper() for code in fener_codes])):
                    rows.append({
                        'GameID': game_code_int,
                        'Player': player.get('Player', player.get('PlayerName')),
                        'Minutes': player.get('Minutes', player.get('Min')),
                        'Points': player.get('Points', player.get('Pts')),
                        'IsStarter': player.get('IsStarter'),
                        'TotalRebounds': player.get('TotalRebounds'),
                        'Assistances': player.get('Assistances'),
                        'Valuation': player.get('Valuation'),
                        'Plusminus': player.get('Plusminus')
                    })
        time.sleep(1)  # Sleep to avoid rate limits
    except Exception as e:
        print(f"Error fetching player boxscore for game {game_code}: {e}")

df = pd.DataFrame(rows)
df.to_csv('fenerbahce_player_boxscores.csv', index=False)
print('Saved Fenerbahce player boxscores to fenerbahce_player_boxscores.csv')
print(df.head())
print(f"Total Fenerbahce player rows: {len(df)}")
    