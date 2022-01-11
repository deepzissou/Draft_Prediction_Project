SELECT  * 
from college_stats
LEFT JOIN stats on college_stats.Player = stats.Player;