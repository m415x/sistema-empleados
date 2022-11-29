CREATE DATABASE IF NOT EXISTS sistema;
USE sistema;
DROP TABLE IF NOT EXISTS empleados;

CREATE TABLE IF NOT EXISTS empleados (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    correo VARCHAR(255),
    foto VARCHAR(5000),
);

-- INSERT INTO empleados (nombre, correo, foto) VALUES ('Test', 'test@email.com', 'foto.jpg');

-- SELECT * FROM empleados;