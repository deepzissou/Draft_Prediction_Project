SELECT *
FROM combined_ncaa_player_stats
LEFT JOIN stats on combined_ncaa_player_stats.name = stats.name
WHERE is_pro = '1';
