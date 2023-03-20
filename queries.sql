use volleyball;
-- 10 Strongest Hitter
SELECT player_name, country, hitters.num_hits - hitters.hit_faults AS hit_efficiency
  FROM hitters JOIN player 
  ON hitters.player_id = player.player_id
  ORDER BY hit_efficiency DESC
  LIMIT 10;

-- 10 Strongest Defensive Countries
SELECT country, SUM(passers.num_digs) - 
                SUM(passers.dig_faults) +
                SUM(passers.num_receptions) - 
                SUM(passers.num_reception_faults) +
                SUM(blockers.num_blocks) - 
                SUM(blockers.block_faults) AS defensive_efficiency
  FROM passers JOIN blockers JOIN player
  ON passers.player_id = player.player_id AND blockers.player_id = player.player_id
  GROUP BY country
  ORDER BY defensive_efficiency DESC
  LIMIT 10;

-- 5 Strongest Shirt Numbers
SELECT shirt_number, SUM(scorers.attacks) + SUM(scorers.blocks) +
                     SUM(scorers.serves) AS overall_efficiency
  FROM scorers JOIN player
  ON scorers.player_id = player.player_id
  GROUP BY shirt_number
  ORDER BY overall_efficiency DESC
  LIMIT 5;
                    