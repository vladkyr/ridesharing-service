-- Drop any existing data and create empty tables
-- Initialize the database

--DROP DATABASE if exists knights;

--CREATE DATABASE knights;
--use knights;

CREATE TABLE favorite_colors (
  name VARCHAR(20),
  color VARCHAR(10)
);

INSERT INTO favorite_colors (name_p, color) VALUES ('Lancelot', 'blue');

INSERT INTO
  favorite_colors (name, color)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');