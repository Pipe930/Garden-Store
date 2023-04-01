

CREATE TABLE USER(
    id_user INT(10) NOT NULL,
    first_name VARCHAR(20) NULL,
    last_name VARCHAR(20) NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(16) NOT NULL,
    last_login DATE NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    date_joined DATE NOT NULL,
    
    CONSTRAINT pk_id_user PRIMARY KEY (id_user)
);

ALTER TABLE USER MODIFY id_user INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE SUBSCRIPTION(
    id_subsciption INT(10) NOT NULL,
    username VARCHAR(40) NOT NULL,
    email VARCHAR(100) NOT NULL,
    amount INT(6) NOT NULL,
    id_user INT(10) NOT NULL,
    
    CONSTRAINT pk_id_subsciption PRIMARY KEY (id_subsciption),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE SUBSCRIPTION MODIFY id_subsciption INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE TOKEN(
    key INT(40) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    id_user INT(10) NOT NULL,
    
    CONSTRAINT pk_key PRIMARY KEY (key),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

CREATE TABLE CART(
    id_cart INT(10) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total_price INT(10) NOT NULL,
    id_user INT(10) NOT NULL,
    
    CONSTRAINT pk_id_cart PRIMARY KEY (id_cart),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE CART MODIFY id_cart INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE CATEGORY(
    id_category INT(10) NOT NULL,
    name VARCHAR(10) NOT NULL,
    description VARCHAR(255) NULL,
    
    CONSTRAINT pk_id_category PRIMARY KEY (id_category)
);

ALTER TABLE CATEGORY MODIFY id_category INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE OFFER(
    id_offer INT(10) NOT NULL,
    name VARCHAR(40) NOT NULL,
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

CREATE TABLE ITEMS(
    id_items INT(20) NOT NULL,
    price INT(10) NOT NULL,
    quantity INT(6) NOT NULL,
    id_cart INT(10) NOT NULL,
    id_product INT(10) NOT NULL,
    
    CONSTRAINT pk_id_items PRIMARY KEY (id_items),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart),
    CONSTRAINT fk_id_product FOREIGN KEY (id_product) REFERENCES PRODUCT(id_product)
);

ALTER TABLE ITEMS MODIFY id_items INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE TYPE_PAYMENT(
    id_type_payment INT(10) NOT NULL,
    name VARCHAR(10) NOT NULL,
    
    CONSTRAINT pk_id_type_payment PRIMARY KEY (id_type_payment)
);

ALTER TABLE TYPE_PAYMENT MODIFY id_type_payment INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE VOUCHER(
    id_voucher INT(10) NOT NULL,
    code VARCHAR(32) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    total_price INT(10) NOT NULL,
    id_cart INT(10) NOT NULL,
    id_user INT(10) NOT NULL,
    id_type_payment INT(10) NOT NULL,
    
    CONSTRAINT pk_id_voucher PRIMARY KEY (id_voucher),
    CONSTRAINT fk_id_cart FOREIGN KEY (id_cart) REFERENCES CART(id_cart),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user),
    CONSTRAINT fk_id_type_payment FOREIGN KEY (id_type_payment) REFERENCES TYPE_PAYMENT(id_type_payment)
);

ALTER TABLE VOUCHER MODIFY id_voucher INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE REGION(
    id_region INT(10) NOT NULL,
    name VARCHAR(40) NOT NULL,
    initials VARCHAR(6) NOT NULL,
    
    CONSTRAINT pk_id_region PRIMARY KEY (id_region)
);

ALTER TABLE REGION MODIFY id_region INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE PROVINCE(
    id_province INT(10) NOT NULL,
    name INT(10) NOT NULL,
    id_region INT(10) NOT NULL,
    
    CONSTRAINT pk_id_province PRIMARY KEY (id_province),
    CONSTRAINT fk_id_region FOREIGN KEY (id_region) REFERENCES REGION(id_region)
);

ALTER TABLE PROVINCE MODIFY id_province INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE COMMUNE(
    id_commune INT(10) NOT NULL,
    name VARCHAR(40) NOT NULL,
    id_province INT(10) NOT NULL,
    
    CONSTRAINT pk_id_commune PRIMARY KEY (id_commune),
    CONSTRAINT fk_id_province FOREIGN KEY (id_province) REFERENCES PROVINCE(id_province)
);

ALTER TABLE COMMUNE MODIFY id_commune INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE ORDER(
    id_order INT(10) NOT NULL,
    code VARCHAR(32) NOT NULL,
    created timestamp NOT NULL DEFAULT current_timestamp,
    condition VARCHAR(20) NOT NULL,
    withdrawal VARCHAR(20) NOT NULL,
    direction VARCHAR(100) NOT NULL,
    num_department INT(10) NULL,
    id_commune INT(10) NOT NULL,
    id_voucher INT(10) NOT NULL,
    
    CONSTRAINT pk_id_order PRIMARY KEY (id_order),
    CONSTRAINT fk_id_commune FOREIGN KEY (id_commune) REFERENCES COMMUNE(id_commune),
    CONSTRAINT fk_id_voucher FOREIGN KEY (id_voucher) REFERENCES VOUVHER(id_voucher)
);

ALTER TABLE ORDER MODIFY id_order INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;

CREATE TABLE DETAIL_ORDER(
    id_detail_order INT(10) NOT NULL,
    id_order INT(10) NOT NULL,
    id_user INT(10) NOT NULL,
    
    CONSTRAINT pk_id_detail_order PRIMARY KEY (id_detail_order),
    CONSTRAINT fk_id_order FOREIGN KEY (id_order) REFERENCES ORDER(id_order),
    CONSTRAINT fk_id_user FOREIGN KEY (id_user) REFERENCES USER(id_user)
);

ALTER TABLE DETAIL_ORDER MODIFY id_detail_order INT(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT = 1;