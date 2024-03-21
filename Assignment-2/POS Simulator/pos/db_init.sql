-- Clear existing data
DELETE FROM products;

-- Create the products table if it doesn't exist
CREATE TABLE IF NOT EXISTS products
(
    name          TEXT,
    price         REAL,
    product_count INTEGER,
    pack_size     INTEGER
);

-- Insert new records
INSERT INTO products (name, price, product_count, pack_size)
VALUES ('Apple', 10.0, 1, NULL);

INSERT INTO products (name, price, product_count, pack_size)
VALUES ('Cola', 2.0, 1, 10);

INSERT INTO products (name, price, product_count, pack_size)
VALUES ('PC', 2500.0, 1, NULL);

INSERT INTO products (name, price, product_count, pack_size)
VALUES ('ChocoPie', 6.5, 3, NULL);

INSERT INTO products (name, price, product_count, pack_size)
VALUES ('Pepsi', 2.0, 1, 3);

INSERT INTO products (name, price, product_count, pack_size)
VALUES ('Pizza', 20.0, 1, NULL);
