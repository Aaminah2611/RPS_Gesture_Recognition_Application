
-- All Players' results:
SELECT u.id AS 'User ID'
    ,u.username AS 'Username'
    ,g.id AS 'Game ID'
    ,g.status AS 'Game Status'
    ,p.player_number AS 'Player Number'
    ,p.gesture AS 'Gesture'
FROM User u
JOIN Participant p ON p.user_id = u.id
JOIN Game g ON g.id = p.game_id;