-- Drop any existing data and create empty tables
-- Initialize the database

--DROP DATABASE if exists knights;

--CREATE DATABASE knights;
--use knights;

CREATE TABLE favorite_colors (
  name VARCHAR(20),
  color VARCHAR(10)
);

INSERT INTO favorite_colors (name, color) VALUES ('Lancelot', 'blue');

INSERT INTO
  favorite_colors (name, color)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');

INSERT INTO favorite_colors (name, color) VALUES ('Lancelot', 'blue');
INSERT INTO favorite_colors (name, color) VALUES ('Galahad', 'yellow');
INSERT INTO favorite_colors (name, color)
VALUES ('Bob', 'black'),
       ('Sam', 'white');




#cursor.execute('SELECT TABLE_NAME FROM information_schema.TABLES')
#cursor.execute('SELECT DISTINCT TABLE_SCHEMA FROM information_schema.TABLES')

