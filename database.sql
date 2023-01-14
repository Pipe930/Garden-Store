CREATE DATABASE gardenstore;

USE gardenstore

CREATE TABLE CATEGORY(
    id_category INT(4) NOT NULL,
    name_category VARCHAR(40) NOT NULL,
    description_category TEXT NOT NULL,

    CONSTRAINT pk_id_category PRIMARY KEY (id_category)
);

ALTER TABLE CATEGORY MODIFY id_category INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE OFFER(
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
    created timestamp NOT NULL DEFAULT current_timestamp,
    id_category INT(4) NOT NULL,
    id_offer INT(4) NOT NULL,

    CONSTRAINT pk_id_prodruct PRIMARY KEY (id_prodruct),
    CONSTRAINT fk_id_category FOREIGN KEY (id_category) REFERENCES CATEGORY(id_category),
    CONSTRAINT fk_id_offer FOREIGN KEY (id_offer) REFERENCES CATEGORY(id_offer)
);

ALTER TABLE PRODUCT MODIFY id_prodruct INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE USER(
    id_user INT(4) NOT NULL,
    username VARCHAR(60) NOT NULL,
    email VARCHAR(100) NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    date_joined DATE NOT NULL,
    is_active BOOLEAN(1) NOT NULL,
    is_staff BOOLEAN(1) NOT NULL,

    CONSTRAINT pk_id_user PRIMARY KEY (id_user)
);

ALTER TABLE USER MODIFY id_user INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE SUBSCRIPTION(
    id_subscription INT(4) NOT NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL,
    amount INT(5) NOT NULL,
    id_user INT(4) NOT NULL,

    CONSTRAINT pk_id_subscription PRIMARY KEY (id_subscription),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE SUBSCRIPTION MODIFY id_subscription INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CART(
    id_cart INT(4) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total INT(10) NOT NULL,
    id_user INT(4) NOT NULL,

    CONSTRAINT pk_id_cart PRIMARY KEY (id_cart),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user) 
);

ALTER TABLE CART MODIFY id_cart INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CARTITEM(
    id_cartitem INT(4) NOT NULL,
    id_cart INT(4) NOT NULL,
    products JSON NOT NULL,
    quantity INT(5) NOT NULL,
    price INT(10) NOT NULL,

    CONSTRAINT pk_id_cartitem PRIMARY KEY (id_cartitem),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart),
    CONSTRAINT fk_products FOREIGN KEY (products) REFERENCES PRODUCT(id_prodruct)
);

ALTER TABLE CARTITEM MODIFY id_cartitem INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE ORDER(
    id_order INT(4) NOT NULL,
    code VARCHAR(100) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    condition VARCHAR(20) NOT NULL,
    withdrawal VARCHAR(20) NOT NULL,
    type_of_pay VARCHAR(20) NOT NULL,
    direction VARCHAR(100) NOT NULL,
    id_user INT(4) NOT NULL,

    CONSTRAINT pk_id_order PRIMARY KEY (id_order),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE ORDER MODIFY id_order INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE VOUCHER(
    id_voucher INT(4) NOT NULL,
    code VARCHAR(100) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total_price INT(10) NOT NULL,
    id_user INT(4) NOT NULL,
    id_cart INT(4) NOT NULL,

    CONSTRAINT pk_id_voucher PRIMARY KEY (id_voucher),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart)
);

ALTER TABLE VOUCHER MODIFY id_voucher INT(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;