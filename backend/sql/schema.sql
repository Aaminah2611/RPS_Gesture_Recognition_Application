CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255)
);

CREATE TABLE Game (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id_1 INT NOT NULL,
    user_id_2 INT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'ongoing', 'finished') DEFAULT 'pending',
    FOREIGN KEY (user_id_1) REFERENCES Users(id),
    FOREIGN KEY (user_id_2) REFERENCES Users(id)
);
