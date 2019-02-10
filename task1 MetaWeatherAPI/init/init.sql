CREATE TABLE IF NOT EXISTS weather_info(
	id BIGINT PRIMARY KEY NOT NULL,
	weather_state_name TEXT NOT NULL,
	weather_state_abbr TEXT NOT NULL,
	wind_direction_compass TEXT NOT NULL,
	created TEXT NOT NULL,
	applicable_date DATE NOT NULL,
	min_temp REAL NOT NULL,
	max_temp REAL NOT NULL,
	the_temp REAL NOT NULL,
	win_speed REAL NOT NULL,
	wind_direction REAL NOT NULL,
	air_pressure REAL NOT NULL,
	humidity INTEGER NOT NULL,
	visibility REAL NULL,
	predictability INTEGER NOT NULL
);