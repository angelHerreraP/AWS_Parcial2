-- Este archivo será copiado automáticamente a la EC2 y ejecutado en la RDS por el script de user_data
-- Puedes mantener aquí la versión más reciente de tu estructura y datos de ejemplo

CREATE DATABASE IF NOT EXISTS my_Library;
USE my_Library;

-- Members Table
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    join_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    biography TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    published_date DATE,
    isbn VARCHAR(20) UNIQUE,
    pages INT,
    category_id INT NOT NULL,
    author_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- Datos de ejemplo
INSERT INTO members (name, email) VALUES
('Juan Pérez', 'juan@example.com'),
('Ana López', 'ana@example.com');

INSERT INTO authors (name, biography) VALUES
('Gabriel García Márquez', 'Autor colombiano, Nobel de Literatura.'),
('Jane Austen', 'Novelista inglesa.');

INSERT INTO categories (name) VALUES
('Novela'),
('Ciencia Ficción');

INSERT INTO books (title, published_date, isbn, pages, category_id, author_id) VALUES
('Cien años de soledad', '1967-05-30', '978-3-16-148410-0', 417, 1, 1),
('Orgullo y prejuicio', '1813-01-28', '978-1-23-456789-7', 279, 1, 2);

INSERT INTO loans (book_id, member_id, loan_date, return_date) VALUES
(1, 1, '2025-07-01', NULL),
(2, 2, '2025-07-10', '2025-07-20');
