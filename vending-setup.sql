DROP TABLE IF EXISTS nutrition;
DROP TABLE IF EXISTS vending_machine_snack;
DROP TABLE IF EXISTS vending_machine;
DROP TABLE IF EXISTS snack;
DROP TABLE IF EXISTS location;

CREATE TABLE location (
    location_id SMALLINT UNSIGNED PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    address_2 VARCHAR(50),
    zip VARCHAR(15) NOT NULL,
    state CHAR(2) NOT NULL
);

CREATE TABLE snack (
    snack_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(45) NOT NULL
);

CREATE TABLE vending_machine (
    machine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id SMALLINT UNSIGNED,
    FOREIGN KEY (location_id) REFERENCES location (location_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE vending_machine_snack (
    snack_id SMALLINT UNSIGNED NOT NULL,
    machine_id SMALLINT UNSIGNED NOT NULL,
    slot_code VARCHAR(3) NOT NULL,
    quantity TINYINT UNSIGNED DEFAULT 0,
    price DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY (machine_id, slot_code),
    FOREIGN KEY (machine_id) REFERENCES vending_machine (machine_id),
    FOREIGN KEY (snack_id) REFERENCES snack (snack_id)
);

CREATE TABLE nutrition (
    snack_id SMALLINT UNSIGNED PRIMARY KEY,
    serving_size VARCHAR(45) NOT NULL,
    serving_per SMALLINT NOT NULL,
    calories SMALLINT NOT NULL,
    total_fat SMALLINT NOT NULL,
    saturated_fat SMALLINT,
    trans_fat SMALLINT,
    cholesterol SMALLINT NOT NULL,
    sodium SMALLINT NOT NULL,
    total_carbohydrate SMALLINT NOT NULL,
    fiber SMALLINT,
    total_sugars SMALLINT,
    added_sugars SMALLINT,
    protein SMALLINT NOT NULL,
    additional_info VARCHAR(300),
    FOREIGN KEY (snack_id) REFERENCES snack (snack_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
