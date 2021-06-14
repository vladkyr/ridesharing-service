DROP TABLE if exists models;
DROP TABLE if exists vehicles;
DROP TABLE if exists users;
DROP TABLE if exists orders;
DROP TABLE if exists history_orders;


CREATE TABLE models (
  model_id int unsigned not null auto_increment primary key,
  manufacturer varchar(30) not null,
  model varchar(20) not null,
  capacity tinyint unsigned not null
);

CREATE TABLE vehicles (
  vehicle_id int unsigned not null auto_increment primary key,
  model_id int unsigned not null,
  status varchar(20),
  number_plate varchar(20) not null,
  foreign key (model_id) references models(model_id)
);

CREATE TABLE users (
  user_id int unsigned not null auto_increment primary key,
  name VARCHAR(30) not null,
  email VARCHAR(40) not null,
  password VARCHAR(40) not null,
  balance smallint unsigned
);

CREATE TABLE orders (
  order_id int unsigned not null auto_increment primary key,
  user_id int unsigned not null,
  vehicle_id int unsigned,
  start_loc varchar(50) not null,
  destination varchar(50) not null,
  status varchar(20),
  passengers smallint unsigned,
  foreign key (user_id) references users(user_id),
  foreign key (vehicle_id) references vehicles(vehicle_id)
);

CREATE TABLE history_orders (
  order_id int unsigned not null primary key,
  user_id int unsigned not null,
  vehicle_id int unsigned,
  start_loc varchar(50) not null,
  destination varchar(50) not null,
  passengers smallint unsigned not null,
  end_time timestamp,
  distance int unsigned not null,
  trip_time int unsigned not null,
  price int unsigned,
  foreign key (user_id) references users(user_id),
  foreign key (vehicle_id) references vehicles(vehicle_id)
);