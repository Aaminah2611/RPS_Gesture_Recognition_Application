CREATE TABLE User (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255)
);

CREATE TABLE Game (
  id INT AUTO_INCREMENT PRIMARY KEY,
  started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status ENUM('pending', 'ongoing', 'finished') DEFAULT 'pending'
);

CREATE TABLE Participant (
  user_id INT REFERENCES User(id),
  game_id INT REFERENCES Game(id),
  role ENUM('player1', 'player2'),
  PRIMARY KEY (user_id, game_id, role),
  gesture VARCHAR(255) DEFAULT NULL
);
