TABLE_CONFIG = {
    'VISITORS': {
        'stage_table': 'VISITORS_STAGE',
        'file': 'visitors.csv',
        'columns': 'full_name, email, phone, address, visitor_id_external',
        'transient_columns': 'visitor_id_external, full_name, email, phone, address',
        'transfer_columns': 'full_name, email, phone, address, visitor_id_external',
        'conditions': "1=1",
        'joins': ""
    },
    'TICKETS': {
        'stage_table': 'TICKET_STAGE',
        'file': 'tickets.csv',
        'columns': 'visitor_id, purchase_date, ticket_type, price, status, ticket_id_external',
        'transient_columns': 'ticket_id_external, visitor_id_external, purchase_date, ticket_type, price, status',
        'transfer_columns': 'v.visitor_id, purchase_date, ticket_type, price, status, ticket_id_external',
        'conditions': "TICKET_STAGE.ticket_type IN ('General', 'VIP', 'Season Pass', 'Student', 'Senior') AND TICKET_STAGE.status IN ('Active', 'Used', 'Expired')",
        'joins': "JOIN VISITORS v ON TICKET_STAGE.visitor_id_external = v.visitor_id_external"
    },
    'ATTRACTIONS': {
        'stage_table': 'ATTRACTIONS_STAGE',
        'file': 'attractions.csv',
        'columns': 'name, type, status, capacity, created_at, attraction_id_external',
        'transient_columns': 'attraction_id_external, name, type, status, capacity, created_at',
        'transfer_columns': 'name, type, status, capacity, created_at, attraction_id_external',
        'conditions': "ATTRACTIONS_STAGE.status IN ('Operational', 'Closed', 'Maintenance')",
        'joins': ""
    },
    'ROLES': {
        'stage_table': 'ROLES_STAGE',
        'file': 'roles.csv',
        'columns': 'role_name, role_id_external',
        'transient_columns': 'role_id_external, role_name',
        'transfer_columns': 'role_name, role_id_external',
        'conditions': "1=1",
        'joins': ""
    },
    'EMPLOYEES': {
        'stage_table': 'EMPLOYEES_STAGE',
        'file': 'employees.csv',
        'columns': 'role_id, full_name, email, phone, hire_date, salary, status, employee_id_external',
        'transient_columns': 'employee_id_external, role_id_external, full_name, email, phone, hire_date, salary, status',
        'transfer_columns': 'r.role_id, full_name, email, phone, hire_date, salary, status, employee_id_external',
        'conditions': "EMPLOYEES_STAGE.status IN ('Active', 'On Leave', 'Resigned')",
        'joins': "JOIN ROLES r ON EMPLOYEES_STAGE.role_id_external = r.role_id_external"
    },
    'ESTABLISHMENTS': {
        'stage_table': 'ESTABLISHMENTS_STAGE',
        'file': 'establishments.csv',
        'columns': 'name, category, created_at, establishment_id_external',
        'transient_columns': 'establishment_id_external, name, category, created_at',
        'transfer_columns': 'name, category, created_at, establishment_id_external',
        'conditions': "ESTABLISHMENTS_STAGE.category IN ('Restaurant', 'Shop')",
        'joins': ""
    },
    'PRODUCTS': {
        'stage_table': 'PRODUCTS_STAGE',
        'file': 'products.csv',
        'columns': 'establishment_id, name, category, price, product_id_external',
        'transient_columns': 'product_id_external, establishment_id_external, name, category, price',
        'transfer_columns': 'e.establishment_id, PRODUCTS_STAGE.name, PRODUCTS_STAGE.category, PRODUCTS_STAGE.price, PRODUCTS_STAGE.product_id_external',
        'conditions': "PRODUCTS_STAGE.category IN ('Food', 'Merchandise')",
        'joins': "JOIN ESTABLISHMENTS e ON PRODUCTS_STAGE.establishment_id_external = e.establishment_id_external"
    },
    'PROMOTIONS':{
        'stage_table': 'PROMOTIONS_STAGE',
        'file': 'promotions.csv',
        'columns': 'promotion_percent, start_date, end_date, promotion_id_external',
        'transient_columns': 'promotion_id_external, promotion_percent, start_date, end_date',
        'transfer_columns': 'promotion_percent, start_date, end_date, promotion_id_external',
        'conditions': "1=1",
        'joins': ""
    },
    'SALES': {
        'stage_table': 'SALES_STAGE',
        'file': 'sales.csv',
        'columns': 'product_id, promotion_id, quantity, total_price, sale_date, sale_id_external',
        'transient_columns': 'sale_id_external, product_id_external, promotion_id, quantity, total_price, sale_date',
        'transfer_columns': 'p.product_id, SALES_STAGE.promotion_id, SALES_STAGE.quantity, SALES_STAGE.total_price, SALES_STAGE.sale_date, SALES_STAGE.sale_id_external',
        'conditions': "SALES_STAGE.quantity > 0",
        'joins': "JOIN PRODUCTS p ON SALES_STAGE.product_id_external = p.product_id_external LEFT JOIN PROMOTIONS pr ON SALES_STAGE.promotion_id = pr.promotion_id"
    },
    'TRANSACTIONS': {
        'stage_table': 'TRANSACTIONS_STAGE',
        'file': 'transactions.csv',
        'columns': 'sale_id, employee_id, visitor_id, amount, transaction_type, transaction_date, transaction_id_external',
        'transient_columns': 'transaction_id_external, sale_id_external, employee_id_external, visitor_id_external, amount, transaction_type, transaction_date',
        'transfer_columns': 'sa.sale_id, e.employee_id, v.visitor_id, TRANSACTIONS_STAGE.amount, TRANSACTIONS_STAGE.transaction_type, TRANSACTIONS_STAGE.transaction_date, TRANSACTIONS_STAGE.transaction_id_external',
        'conditions': "TRANSACTIONS_STAGE.transaction_type IN ('Ticket Sale', 'Product Sale', 'Refund')",
        'joins': "LEFT JOIN EMPLOYEES e ON TRANSACTIONS_STAGE.employee_id_external = e.employee_id_external LEFT JOIN VISITORS v ON TRANSACTIONS_STAGE.visitor_id_external = v.visitor_id_external LEFT JOIN SALES sa ON TRANSACTIONS_STAGE.sale_id_external = sa.sale_id_external"
    }
}
