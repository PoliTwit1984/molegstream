from pydfs_lineup_optimizer import get_optimizer, Site, Sport, CSVLineupExporter, Player

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASKETBALL)
optimizer.load_players_from_csv("rename.csv")

for lineup in optimizer.optimize(n=2):
    print(lineup)
    print(lineup.players)  # list of players
    print(lineup.fantasy_points_projection)
    print(lineup.salary_costs)




# from draft_kings import Client
# from draft_kings.data import Sport
# details = Client().available_players(draft_group_id=69739)

# print(details.players[0])
