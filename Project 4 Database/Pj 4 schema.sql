DROP TABLE IF EXISTS college_stats;

CREATE TABLE college_stats (
	Player VARCHAR NOT NULL,
	Class INT NOT NULL,
	Pos VARCHAR NOT NULL,
	School VARCHAR NOT NULL,
	Conf VARCHAR NOT NULL,
	Drafted INT NOT NULL
);

DROP TABLE IF EXISTS stats;

CREATE TABLE stats (
	Player VARCHAR NOT NULL,
	height INT,
	weight INT,
	NCAA__3ptapg DECIMAL,
	NCAA_fgapg DECIMAL,
	NCAA_ftapg DECIMAL,
	NCAA_ppg DECIMAL,
	NBA__3ptapg DECIMAL,
	NBA_fga_per_game DECIMAL,
	NBA_fta_p_g DECIMAL,
	NBA_ppg DECIMAL
);

DROP TABLE IF EXISTS combined_ncaa_player_stats;

CREATE TABLE combined_ncaa_player_stats (
	url VARCHAR,
	name VARCHAR,
	fgapg DECIMAL,
	fgpct DECIMAL,
	fgpg DECIMAL,
	ftapg DECIMAL,
	ftpct DECIMAL,
	ftpg DECIMAL,
	games INT,
	height Decimal,
	pfpg DECIMAL,
	ptspg DECIMAL,
	sospg Decimal,
	trbpg Decimal,
	is_pro INT
);