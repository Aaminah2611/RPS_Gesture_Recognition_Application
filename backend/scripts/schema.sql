CREATE TABLE User (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Game (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'ongoing', 'finished') DEFAULT 'pending'
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
