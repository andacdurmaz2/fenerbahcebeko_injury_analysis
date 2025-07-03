from euroleague_api.shot_data import ShotData
from euroleague_api.player_stats import PlayerStats
season = 2022
game_code = 1
competition_code = "E"

shotdata = ShotData(competition_code)
playerstats = PlayerStats()

df = playerstats.get_player_stats_all_seasons("traditional")
filtered_df = df[df['player.team.name'].str.contains('Fener')]

print(filtered_df)
print('Number of players: '  + str(len(filtered_df)))