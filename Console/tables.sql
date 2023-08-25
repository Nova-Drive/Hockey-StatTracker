DROP TABLE IF EXISTS games;
--DROP VIEW IF EXISTS career;


CREATE TABLE games ( 
id INTEGER,
character VARCHAR(20),
season INTEGER,
result VARCHAR(4),
shots INTEGER,
saves INTEGER,
league VARCHAR(5),
opp_team VARCHAR(4),
curr_team VARCHAR(4),
pushups INT,
PRIMARY KEY (id),
FOREIGN KEY (character) REFERENCES characters(name));

DROP TABLE IF EXISTS data;
CREATE TABLE data (
league CHAR(3),
team VARCHAR(4),
season INTEGER,
character VARCHAR(20),
FOREIGN KEY (character) REFERENCES characters(name));

DROP TABLE IF EXISTS characters;
CREATE TABLE characters (
name VARCAR(20),
position VARCHAR(10),
number INTEGER,
PRIMARY KEY (name));

-- Relook into displaying stats for each season plus with career and team stats

DROP VIEW IF EXISTS career;
CREATE VIEW career (saves, shots, svpct, seasons, tot_games, num_wins, num_loss, num_otl, winpct, pu)
AS
SELECT SUM(saves), SUM(shots), CAST(SUM(saves) AS REAL)/CAST(SUM(shots) AS REAL),
(SELECT MAX(season) FROM games), COUNT(id),
(SELECT COUNT(*) FROM games WHERE result = "WIN"),
(SELECT COUNT(*) FROM games WHERE result = "LOSS"),
(SELECT COUNT(*) FROM games WHERE result = "OTL"),
CAST((SELECT COUNT(*) FROM games WHERE result = "WIN") AS REAL) / CAST(COUNT(result) AS REAL), SUM(pushups)
FROM games;