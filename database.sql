CREATE DATABASE gardenstore;

USE gardenstore

CREATE TABLE CATEGORY(
    id_category INT(10) NOT NULL,
    name_category VARCHAR(40) NOT NULL,
    description_category TEXT NOT NULL,

    CONSTRAINT pk_id_category PRIMARY KEY (id_category)
);

ALTER TABLE CATEGORY MODIFY id_category INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE OFFER(
    id_offer INT(10) NOT NULL,
    name_offer VARCHAR(40) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    discount INT(3) NOT NULL,

    CONSTRAINT pk_id_offer PRIMARY KEY (id_offer)
);

ALTER TABLE OFFER MODIFY id_offer INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE PRODUCT(
    id_prodruct INT(10) NOT NULL,
    name_product VARCHAR(40) NOT NULL,
    price INT(10) NOT NULL,
    stock INT(5) NOT NULL,
    image BLOB NOT NULL,
    description TEXT,
    slug VARCHAR(255) NOT NULL,
    condition BOOLEAN NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    id_category INT(10) NOT NULL,
    id_offer INT(10) NOT NULL,

    CONSTRAINT pk_id_prodruct PRIMARY KEY (id_prodruct),
    CONSTRAINT fk_id_category FOREIGN KEY (id_category) REFERENCES CATEGORY(id_category),
    CONSTRAINT fk_id_offer FOREIGN KEY (id_offer) REFERENCES CATEGORY(id_offer)
);

ALTER TABLE PRODUCT MODIFY id_prodruct INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE USER(
    id_user INT(10) NOT NULL,
    username VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    date_joined DATE NOT NULL,
    is_active BOOLEAN(1) NOT NULL,
    is_staff BOOLEAN(1) NOT NULL,

    CONSTRAINT pk_id_user PRIMARY KEY (id_user)
);

ALTER TABLE USER MODIFY id_user INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE TOKEN (
    id_token INT(10) NOT NULL,
    key VARCHAR(40) NOT NULL,
    id_user INT(10) NOT NULL,

    CONSTRAINT pk_id_token PRIMARY KEY (id_token),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE TOKEN MODIFY id_token INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE SUBSCRIPTION(
    id_subscription INT(10) NOT NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    amount INT(5) NOT NULL,
    id_user INT(10) NOT NULL,

    CONSTRAINT pk_id_subscription PRIMARY KEY (id_subscription),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE SUBSCRIPTION MODIFY id_subscription INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CART(
    id_cart INT(10) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total INT(10) NOT NULL,
    id_user INT(4) NOT NULL,

    CONSTRAINT pk_id_cart PRIMARY KEY (id_cart),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user) 
);

ALTER TABLE CART MODIFY id_cart INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CARTITEM(
    id_cartitem INT(10) NOT NULL,
    id_cart INT(10) NOT NULL,
    products JSON NOT NULL,
    quantity INT(5) NOT NULL,
    price INT(10) NOT NULL,

    CONSTRAINT pk_id_cartitem PRIMARY KEY (id_cartitem),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart),
    CONSTRAINT fk_products FOREIGN KEY (products) REFERENCES PRODUCT(id_prodruct)
);

ALTER TABLE CARTITEM MODIFY id_cartitem INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE COMMUNE (
    id_commune INT(10) NOT NULL,
    name_commune VARCHAR(40) NOT NULL,

    CONSTRAINT pk_id_commune PRIMARY KEY (id_commune),
);

ALTER TABLE COMMUNE MODIFY id_commune INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CITY (
    id_city INT(10) NOT NULL,
    name_city VARCHAR(40) NOT NULL,
    id_commune INT(10) NOT NULL,
    
    CONSTRAINT pk_id_city PRIMARY KEY (id_city),
    CONSTRAINT fk_id_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune)
);

ALTER TABLE CITY MODIFY id_city INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE REGION (
    id_region INT(10) NOT NULL,
    name_region VARCHAR(100) NOT NULL,
    initials VARCHAR(10) NOT NULL,
    id_city INT(10) NOT NULL,

    CONSTRAINT pk_id_region PRIMARY KEY (id_region),
    CONSTRAINT fk_id_city FOREIGN KEY (id_city) REFERENCES CITY(id_city)
);

ALTER TABLE REGION MODIFY id_region INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE ADDRESS (
    id_address INT(10) NOT NULL,
    address VARCHAR(100) NOT NULL,
    num_department INT(6) NOT NULL,
    id_region INT(10) NOT NULL,

    CONSTRAINT pk_id_address PRIMARY KEY (id_address),
    CONSTRAINT fk_id_region FOREIGN KEY (id_region) REFERENCES REGION(id_region)
);

ALTER TABLE ADDRESS MODIFY id_address INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE ORDER(
    id_order INT(10) NOT NULL,
    code VARCHAR(100) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    condition VARCHAR(20) NOT NULL,
    withdrawal VARCHAR(20) NOT NULL,
    id_user INT(4) NOT NULL,
    id_address INT()

    CONSTRAINT pk_id_order PRIMARY KEY (id_order),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE ORDER MODIFY id_order INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE VOUCHER(
    id_voucher INT(10) NOT NULL,
    code VARCHAR(100) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total_price INT(10) NOT NULL,
    id_user INT(4) NOT NULL,
    id_cart INT(4) NOT NULL,

    CONSTRAINT pk_id_voucher PRIMARY KEY (id_voucher),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart)
);

ALTER TABLE VOUCHER MODIFY id_voucher INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;