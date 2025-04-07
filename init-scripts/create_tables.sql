CREATE DATABASE IF NOT EXISTS mahjong;

USE mahjong;

CREATE TABLE IF NOT EXISTS member (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    rank INT NOT NULL,
    score INT NOT NULL
);

-- 初期データの挿入
INSERT INTO member (name, rank, score) VALUES
    ('kisen', 1, 1500);
