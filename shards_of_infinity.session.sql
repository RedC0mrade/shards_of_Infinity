-- UPDATE player_card_instances
-- SET player_state_id = 5, zone = 'hand'
-- WHERE id = 27;

-- UPDATE player_states
-- SET heath = 47
-- WHERE id = 2;

UPDATE player_states
SET health = 47
WHERE id = 2;

-- DELETE FROM games
-- WHERE id = 2;

UPDATE player_card_instances
SET player_state_id = 2, zone = 'hand'
WHERE id = 97;

-- SELECT id, card_id, game_id, zone FROM player_card_instances
-- WHERE player_state_id = 6 AND card_id = 319 AND zone = 'hand' AND game_id = 3;