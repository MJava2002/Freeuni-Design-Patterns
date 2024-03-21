-- Clear existing data
DELETE FROM discounts;

-- Create the products table if it doesn't exist
CREATE TABLE IF NOT EXISTS discounts
(
    name          TEXT,
    percentage    INTEGER
);

INSERT INTO discounts (name, percentage)
VALUES ('Cola',  10);

INSERT INTO discounts (name, percentage)
VALUES ('PC', 15);

INSERT INTO discounts (name, percentage)
VALUES ('Pizza', 20);
