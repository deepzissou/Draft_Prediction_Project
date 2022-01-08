SELECT name, fgapg, fgpct, fgpg, ftapg, ftpct, games, height, pfpg, ptspg, sospg, trbpg
FROM combined_ncaa_player_stats
Where is_pro = '1'
Order by name;