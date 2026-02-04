-- UPDATE player_card_instances
-- SET player_state_id = 5, zone = 'hand'
-- WHERE id = 27;

-- UPDATE player_states
-- SET crystals = 20
-- WHERE id = 2;    

-- DELETE FROM games
-- WHERE id = 2;

-- UPDATE player_card_instances
-- SET player_state_id = 6, zone = 'hand'
-- WHERE id = 319;

SELECT id, card_id, game_id, zone FROM player_card_instances
WHERE player_state_id = 6 AND card_id = 319 AND zone = 'hand' AND game_id = 3;