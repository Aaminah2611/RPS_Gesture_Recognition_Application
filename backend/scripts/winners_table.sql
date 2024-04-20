
-- Who Won?
SELECT g.id AS 'Game ID'
    ,p1.gesture AS 'Player 1 Gesture'
    ,p2.gesture AS 'Player 2 Gesture'
    ,CASE 
         WHEN ((p1.gesture = 'rock' AND p2.gesture = 'scissors') OR 
               (p1.gesture = 'paper' AND p2.gesture = 'rock') OR
               (p1.gesture = 'scissors' AND p2.gesture = 'paper')) THEN u1.id
         WHEN ((p2.gesture = 'rock' AND p1.gesture = 'scissors') OR 
               (p2.gesture = 'paper' AND p1.gesture = 'rock') OR
               (p2.gesture = 'scissors' AND p1.gesture = 'paper')) THEN u2.id
         ELSE -1   
     END AS 'Winning User ID'
FROM Game g
JOIN Participant p1 ON p1.game_id = g.id AND p1.player_number = 1
JOIN User u1 ON u1.id = p1.user_id
JOIN Participant p2 ON p2.game_id = g.id AND p2.player_number = 2
JOIN User u2 ON u2.id = p2.user_id;
