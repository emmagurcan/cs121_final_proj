-- Computes the average number of aces a player of a certain country makes.
-- Takes in a country code of length three.x
DELIMITER !

CREATE FUNCTION avg_aces_made (country CHAR(3)) RETURNS INT DETERMINISTIC
BEGIN

DECLARE result INT;

SELECT AVG(num_aces) INTO result 
FROM servers NATURAL JOIN player
WHERE player.country = country
ORDER BY num_aces;

RETURN result;

END !

DELIMITER ;

-- Returns the average number of successful attacks, blocks, and serves made by
-- a player of a chosen shirt number.
DELIMITER !

CREATE FUNCTION score_jersey (jersey TINYINT) RETURNS INT DETERMINISTIC
BEGIN

DECLARE result INT;

SELECT AVG(attacks) + AVG(blocks) + AVG(serves) INTO result
FROM scorers NATURAL JOIN player
WHERE shirt_number = jersey;
RETURN result;

END !

DELIMITER ;

-- Updates the number of serves for a player in scorers when
-- the number of aces in servers is updated.
DELIMITER !

CREATE PROCEDURE sp_volleyball_update_serves(
    new_playerid INT,
    new_aces INT
)

BEGIN 
    UPDATE scorers
        SET serves = serves + new_aces
        WHERE player_id = new_playerid;
END !

-- Triggers only if servers is updated.
CREATE TRIGGER volleyball_update_serves AFTER UPDATE
       ON servers FOR EACH ROW
BEGIN
    CALL sp_volleyball_update_serves(NEW.player_id, NEW.num_aces);
END !

DELIMITER ;
