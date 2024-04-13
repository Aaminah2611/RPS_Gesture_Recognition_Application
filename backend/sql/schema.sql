CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE Game (
    id INTEGER PRIMARY KEY,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);

CREATE TABLE Participant (
    id INTEGER PRIMARY KEY,
    game_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    gesture VARCHAR(50),
    player_number INTEGER,
    FOREIGN KEY (game_id) REFERENCES Game(id),
    FOREIGN KEY (user_id) REFERENCES User(id)
);
