CREATE DATABASE gardenstore;

USE gardenstore

CREATE TABLE CATEGORY (
    id_category INT(4) NOT NULL,
    name_category VARCHAR(40) NOT NULL,
    description_category TEXT NOT NULL,

    CONSTRAINT pk_id_category PRIMARY KEY (id_category)
);

ALTER TABLE CATEGORY MODIFY id_category INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE OFFER (
    id_offer INT(4) NOT NULL,
    name_offer VARCHAR(40) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discount INT(3) NOT NULL,

    CONSTRAINT pk_id_offer PRIMARY KEY (id_offer)
);

ALTER TABLE OFFER MODIFY id_offer INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE PRODUCT(
    id_prodruct INT(4) NOT NULL,
    name_product VARCHAR(40) NOT NULL,
    price INT(10) NOT NULL,
    stock INT(5) NOT NULL,
    image BLOB NOT NULL,
    description TEXT,
    slug VARCHAR(255) NOT NULL,
    condition BOOLEAN NOT NULL,
    create timestamp NOT NULL DEFAULT current_timestamp,
    id_category INT(4) NOT NULL,
    id_offer INT(4) NOT NULL,

    CONSTRAINT pk_id_prodruct PRIMARY KEY (id_prodruct),
    CONSTRAINT fk_id_category FOREIGN KEY (id_category),
    REFERENCES CATEGORY(id_category),
    CONSTRAINT fk_id_offer FOREIGN KEY (id_offer),
    REFERENCES CATEGORY(id_offer)
);

ALTER TABLE PRODUCT MODIFY id_prodruct INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;
