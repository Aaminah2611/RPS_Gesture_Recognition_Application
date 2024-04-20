CREATE TABLE User (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Game (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('running','finished') DEFAULT 'running',
    winner VARCHAR(50)
);

CREATE TABLE Participant (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    gesture VARCHAR(50),
    player_number INTEGER,
    FOREIGN KEY (game_id) REFERENCES Game(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);

INSERT INTO User(username, password) VALUES('fred', 'pass');
INSERT INTO User(username, password) VALUES('barney', 'word');
INSERT INTO User(username, password) VALUES('wilma', 'secure1');

INSERT INTO Game(status) VALUES('finished');
INSERT INTO Game(status) VALUES('finished');
INSERT INTO Game(status) VALUES('finished');

INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(1, 1, 'rock', 1);
INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(1, 2, 'paper', 2);
INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(2, 3, 'scissors', 1);
INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(2, 1, 'paper', 2);
INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(3, 2, 'rock', 1);
INSERT INTO Participant(game_id, user_id, gesture, player_number) VALUES(3, 3, 'rock', 2);


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
