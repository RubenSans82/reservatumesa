CREATE DATABASE reservatumesa;
USE reservatumesa;
CREATE TABLE client (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL
);

CREATE TABLE restaurant (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    restaurant_name VARCHAR(100) NOT NULL,
    capacity INT NOT NULL,
    website VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE reservation (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    diners INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    status ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(client_id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurant(restaurant_id)
);
