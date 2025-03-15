-- Here are all Transient tables. They will accept the data from the py script,
-- Then the records will be filtered and only the ones with valid info will be sent to the
-- actual table. The other records will stay in the Transient Table to be reviewed and analysed

USE DATABASE MEET_ONE;

CREATE OR REPLACE TRANSIENT TABLE VISITORS_STAGE (
    visitor_id_external INT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255)
);

CREATE OR REPLACE TRANSIENT TABLE TICKET_STAGE(
    ticket_id_external INT,
    visitor_id_external INT,
    purchase_date DATE,
    ticket_type STRING,
    price DECIMAL(10,2),
    status VARCHAR(20)
);


CREATE OR REPLACE TRANSIENT TABLE ATTRACTIONS_STAGE(
    attraction_id_external INT,
    name VARCHAR(50),
    type VARCHAR(50), -- CHECK (type IN ('Ferris Wheel', ...))
    status VARCHAR(20), -- CHECK (status IN ('Operational', 'Closed', 'Maintanance')),
    capacity INT, -- CHECK (capacity > 0)
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE OR REPLACE TRANSIENT TABLE ROLES_STAGE (
    role_id_external INT,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE OR REPLACE TRANSIENT TABLE EMPLOYEES_STAGE(
    employee_id_external INT,
    role_id_external INT,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE,
    salary DECIMAL(10,2) NOT NULL,
    status VARCHAR(20)
);

CREATE OR REPLACE TRANSIENT TABLE ESTABLISHMENTS_STAGE(
    establishment_id_external INT,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL, -- CHECK (category IN ('Restaurant', 'Shop'))
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE OR REPLACE TRANSIENT TABLE PRODUCTS_STAGE(
    product_id_external INT,
    establishment_id_external INT NOT NULL, -- Where the product is sold
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL, -- CHECK (category IN ('Food', 'Merchandise'))
    price DECIMAL(10,2) NOT NULL
);

CREATE OR REPLACE TRANSIENT TABLE PROMOTIONS_STAGE (
    promotion_id_external INT,
    promotion_percent INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE OR REPLACE TRANSIENT TABLE SALES_STAGE(
    sale_id_external INT,
    product_id_external INT NOT NULL,
    promotion_id INT,
    quantity INT NOT NULL, -- CHECK (quantity > 0),
    total_price DECIMAL(10,2) NOT NULL,
    sale_date DATE DEFAULT CURRENT_DATE
);

CREATE OR REPLACE TRANSIENT TABLE TRANSACTIONS_STAGE(
    transaction_id_external INT,
    sale_id_external INT,
    employee_id_external INT,
    visitor_id_external INT,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type VARCHAR(50), -- CHECK (transaction_type IN ('Ticket Purchase', 'Food Purchase', 'Merchandise', 'Refund')),
    transaction_date DATE DEFAULT CURRENT_DATE
);