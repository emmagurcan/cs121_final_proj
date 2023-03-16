use volleyball;

DROP TABLE IF EXISTS hitters;
DROP TABLE IF EXISTS passers;
DROP TABLE IF EXISTS setters;
DROP TABLE IF EXISTS blockers;
DROP TABLE IF EXISTS servers;
DROP TABLE IF EXISTS scorers;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
  player_id         SERIAL PRIMARY KEY,
  player_name       VARCHAR(40)     NOT NULL,
  shirt_number      TINYINT         NOT NULL, 
  country           CHAR(3)         NOT NULL,
  league            CHAR(1)         NOT NULL,   
  gender            VARCHAR(20)     NOT NULL
);
-- Represents the number of hits, faults, and hitting percentage for 
-- the top hitters in the men's and women's FIVB league
CREATE TABLE hitters(
  player_id        BIGINT UNSIGNED,
  num_hits         INT            NOT NULL,
  hit_faults       INT            NOT NULL,
  hit_percentage   NUMERIC(4,2)   NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents the number of digs and serve receives for the top liberos
-- in the men's and women's FIVB league
CREATE TABLE passers(
  player_id             BIGINT UNSIGNED,
  num_digs              INT    NOT NULL,
  dig_faults            INT    NOT NULL,
  num_receptions        INT    NOT NULL,
  num_reception_faults  INT    NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents the number of sets and faults for the top setters
-- in the men's and women's FIVB league
CREATE TABLE setters(
  player_id          BIGINT UNSIGNED,
  set_attempts       INT    NOT NULL,
  set_faults         INT    NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents the number of blocks, faults, and set average for the top 
-- blockers in the men's and women's FIVB league
CREATE TABLE blockers(
  player_id      BIGINT UNSIGNED,
  num_blocks     INT    NOT NULL,
  block_faults   INT    NOT NULL,
  block_set_avg  INT    NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents the number of aces and faults for the top servers
-- in the men's and women's FIVB league
CREATE TABLE servers(
  player_id    BIGINT UNSIGNED,
  num_aces     INT    NOT NULL,
  num_faults   INT    NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

-- Represents the number of attacks, blocks, and serves
-- for the top scorers in the men's and women's FIVB league
CREATE TABLE scorers(
  player_id    BIGINT UNSIGNED,
  attacks      INT    NOT NULL,
  blocks       INT    NOT NULL,
  serves       INT    NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id) 
  ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX idx_attacks ON scorers(attacks);
