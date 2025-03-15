CREATE DATABASE MEET_ONE;

USE DATABASE MEET_ONE;

--Stage for the csv files 
CREATE OR REPLACE STAGE MY_STAGE
  FILE_FORMAT = (TYPE = CSV 
                 FIELD_OPTIONALLY_ENCLOSED_BY = '"'
                 SKIP_HEADER = 1);

-- Creating file format for the csv files
CREATE OR REPLACE FILE FORMAT MY_CSV_FORMAT
  TYPE = 'CSV'
   FIELD_DELIMITER = ','
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  SKIP_HEADER = 1
  NULL_IF = ('NULL', '');

CREATE OR REPLACE TABLE VISITORS(
    visitor_id INT AUTOINCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255),
    visitor_id_external INT NULL
);

CREATE OR REPLACE TABLE TICKETS(
    ticket_id INT AUTOINCREMENT PRIMARY KEY,
    visitor_id INT NOT NULL,
    purchase_date DATE,
    ticket_type VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (visitor_id) REFERENCES VISITORS(visitor_id),
    ticket_id_external INT NULL
);



CREATE OR REPLACE TABLE ATTRACTIONS(
    attraction_id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    capacity INT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE NOT NULL,
    attraction_id_external INT NULL
);

CREATE OR REPLACE TABLE ROLES(
    role_id INT AUTOINCREMENT PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_id_external INT NULL
);


CREATE OR REPLACE TABLE EMPLOYEES(
    employee_id INT AUTOINCREMENT PRIMARY KEY,
    role_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE,
    salary DECIMAL(10,2) NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (role_id) REFERENCES ROLES(role_id) ON DELETE SET NULL,
    employee_id_external INT NULL
);


CREATE OR REPLACE TABLE ESTABLISHMENTS(
    establishment_id INT AUTOINCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE,
    establishment_id_external INT NULL
);


CREATE OR REPLACE TABLE PRODUCTS(
    product_id INT AUTOINCREMENT PRIMARY KEY,
    establishment_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (establishment_id) REFERENCES ESTABLISHMENTS(establishment_id) ON DELETE SET NULL,
    product_id_external INT NULL
);


CREATE OR REPLACE TABLE PROMOTIONS(
    promotion_id INT AUTOINCREMENT PRIMARY KEY,
    promotion_percent INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    promotion_id_external INT NULL
);


CREATE OR REPLACE TABLE SALES(
    sale_id INT AUTOINCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    promotion_id INT,
    quantity INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id) ON DELETE SET NULL,
    FOREIGN KEY (promotion_id) REFERENCES PROMOTIONS(promotion_id) ON DELETE SET NULL,
    sale_id_external INT NULL
);


CREATE OR REPLACE TABLE TRANSACTIONS(
    transaction_id INT AUTOINCREMENT PRIMARY KEY,
    sale_id INT,
    employee_id INT,
    visitor_id INT,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(50),
    transaction_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (sale_id) REFERENCES SALES(sale_id) ON DELETE SET NULL,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id) ON DELETE SET NULL,
    FOREIGN KEY (visitor_id) REFERENCES VISITORS(visitor_id) ON DELETE SET NULL,
    transaction_id_external INT NULL
);


