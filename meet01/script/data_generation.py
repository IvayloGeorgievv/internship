import random
from datetime import date
from faker import Faker

# Using Faker library to generate fake visitor data
fake = Faker()


def generate_all_data(business_climate):

    # Defining the number of records that are not affected by the business climate
    num_attractions = 20
    num_roles = 5
    num_employees = 80
    num_establishments = 10
    num_products = 30
    num_promotions = 1

    # Depending on the business climate we get randomised number of visitors, equal amount tickets, randomised high number of sales and transactions = sales + tickets
    if business_climate == 'P':
        num_visitors = random.randint(300,400)
        num_tickets = num_visitors
        num_sales = random.randint(100,200)

    else:
        num_visitors = random.randint(100,150)
        num_tickets = num_visitors
        num_sales = random.randint(20,50)

    # Generate the data

    # Needed lists to generate unique names for attractions
    # The idea of putting the lists outside the func is to optimize it because that way it works faster
    # If I had put it inside the func with these static arrays they would have been defined again and again and slow down the func
    adjective_theme = ["Phantom", "Inferno", "Twilight", "Storm", "Eclipse", "Haunted"]
    noun_action = ["Plunge", "Cyclone", "Vortex", "Spiral", "Rush", "Maze"]
    attractions = [generate_attraction_data(i, adjective_theme, noun_action) for i in range(num_attractions)]


    role_names = ['Manager', 'Cashier', 'Operator', 'Security', 'Cleaner']
    roles = [generate_roles_data(i, role_names) for i in range(num_roles)]

    employees = [generate_employee_data(i, random.randint(0, num_roles - 1)) for i in range(num_employees)]

    establishments = [generate_establishment_data(i) for i in range(num_establishments)]

    #Get shops and restaurants so it assigns for example products from type Merch to Shops and so on
    shops = [estab['establishment_id_external'] for estab in establishments if estab['category'] == 'Shop']
    restaurants = [estab['establishment_id_external'] for estab in establishments if estab['category'] == 'Restaurant']
    others = [estab['establishment_id_external'] for estab in establishments if estab['category'] == 'Whatever']

    food_names = ["Burger", "Hot Dog", "Soda", "Coke", "Fries", "Smoothie"]
    merch_names = ["T-shirt", "Hat", "Jacket", "Shoes", "Mug", "Poster"]

    products = []

    # Generate Products and actually assign them correct to the establishments and assign real names
    # That way there won't be a Restaurant selling T-shirts
    for i in range(num_products):
        product = generate_product_item_data(i, 0)

        if product['category'] == 'Food':
            product['name'] = random.choice(food_names)
            product['establishment_id_external'] = random.choice(restaurants)
        elif product['category'] == 'Merchandise':
            product['name'] = random.choice(merch_names)
            product['establishment_id_external'] = random.choice(shops)
        else:
            product['name'] = random.choice(food_names + merch_names)
            product['establishment_id_external'] = random.choice(others)

        products.append(product)

    visitors = [generate_visitor_data(i) for i in range(num_visitors)]
    tickets = [generate_ticket_data(i, visitors[i]['visitor_id_external']) for i in range(num_tickets)]

    promotions = [generate_promotion_data(i) for i in range(num_promotions)]

    sales = []

    #Generate cashiers to use for transactions
    cashiers = get_cashiers(employees, roles)

    #Generate accurate number of Transactions
    transactions = []
    transaction_id = 0

    # Creating dictionary with all needed info to apply a Promotion to a Sale to make the process faster and optimize the script
    active_promotions = {
        promo['promotion_id']: (promo['start_date'], promo['end_date'], promo['promotion_percent'])
        for promo in promotions
    }

    for i in range(num_sales):
        product = random.choice(products)

        sale = generate_sale_data(i,
                                  product['product_id_external'],
                                  0,
                                  random.randint(1, 5),
                                  product['price'])

        for promo_id, (start_date, end_date, percent) in active_promotions.items():
            if start_date <= sale['sale_date'] <= end_date:
                discount = (percent / 100) * sale['total_price']
                sale['total_price'] -= discount
                sale['promotion_id'] = promo_id
                break

        sales.append(sale)

        transactions.append(generate_transactions_data(transaction_id,
                                                       sale['sale_id_external'],
                                                       random.choice(cashiers)['employee_id_external'],
                                                       random.randint(1, num_tickets),
                                                       'Product Sale',
                                                       sale['total_price']))
        transaction_id += 1

    for ticket in tickets:
        transactions.append(generate_transactions_data(transaction_id,
                                                       None,
                                                       random.choice(cashiers)['employee_id_external'],
                                                       ticket['visitor_id_external'],
                                                       'Ticket Sale',
                                                       ticket['price']))
        transaction_id += 1

    #Generate some refunds just for different types of data
    num_refunds = random.randint(0,10)

    for refund in range(num_refunds):
        transactions.append(generate_transactions_data(transaction_id,
                                                       None,
                                                       random.choice(cashiers)['employee_id_external'],
                                                       random.randint(1, num_visitors),
                                                       'Refund',
                                                       random.uniform(10,100)))
        transaction_id += 1


    return attractions, roles, employees, establishments, products, promotions,  visitors, tickets, sales, transactions


def generate_visitor_data(visitor_id):
    return {
        'visitor_id_external': visitor_id,
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number()[:20],
        'address': fake.address()
    }

def generate_ticket_data(ticket_id, visitor_id):
    return {
        'ticket_id_external': ticket_id,
        'visitor_id_external': visitor_id,
        'purchase_date': fake.date(),
        'ticket_type': random.choice(['General', 'VIP', 'Season Pass', 'Student', 'Senior', 'Whatever']),
        'price': round(random.uniform(10, 100), 2),
        'status': random.choice(['Active', 'Used', 'Expired', 'Whatever']),
    }

def generate_attraction_data(attraction_id, adjectives, nouns):
    return {
        'attraction_id_external': attraction_id,
        'name': random.choice(adjectives) + " " + random.choice(nouns),
        'type': random.choice(['Ferris Wheel', 'Roller Coaster', 'Drop Tower', 'Haunted House', 'Whatever']),
        'status': random.choice(['Operational', 'Closed', 'Maintenance', 'Whatever']),
        'capacity': random.randint(5, 20),
        'created_at': fake.date()
    }

# Modified: change 'role_id' to 'role_id_external'
def generate_roles_data(role_id, role_names):
    return {
        'role_id_external': role_id,
        'role_name': role_names[role_id]
    }

# Modified: change 'role_id' to 'role_id_external'
def generate_employee_data(employee_id, role_id):
    return {
        'employee_id_external': employee_id,
        'role_id_external': role_id,
        'full_name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number()[:20],
        'hire_date': fake.date(),
        'salary': round(random.uniform(1500, 5000), 2),
        'status': random.choice(['Active', 'On Leave', 'Resigned', 'Whatever']),
    }

def generate_establishment_data(establishment_id):
    return {
        'establishment_id_external': establishment_id,
        'name': fake.company(),
        'category': random.choice(['Shop', 'Restaurant']),
        'created_at': fake.date_this_decade()
    }

def generate_product_item_data(product_id, establishment_id):
    return {
        'product_id_external': product_id,
        'establishment_id_external': establishment_id,
        'name': ' ',
        'category': random.choice(['Merchandise', 'Food']),
        'price': round(random.uniform(5, 30), 2),
    }

# Modified: update key names to use the external id for role comparisons.
def get_cashiers(employees, roles):
    cashier_role_id = next(role['role_id_external'] for role in roles if role['role_name'] == 'Cashier')
    cashiers = [emp for emp in employees if emp['role_id_external'] == cashier_role_id]
    return cashiers

def generate_promotion_data(promotion_id):
    return {
        'promotion_id': promotion_id,
        'promotion_percent': random.randint(5, 20),
        'start_date': fake.date_between_dates(date_start=date(2024, 11, 30), date_end=date(2025, 1, 31)),
        'end_date': fake.date_between_dates(date_start=date(2025, 2, 28), date_end=date(2025, 4, 30)),
    }

def generate_sale_data(sale_id, product_id, promotion_id, quantity, price_per_item):
    return {
        'sale_id_external': sale_id,
        'product_id_external': product_id,
        'promotion_id': promotion_id,
        'quantity': quantity,
        'total_price': quantity * price_per_item,
        'sale_date': fake.date_this_year()
    }

def generate_transactions_data(transaction_id, sale_id, employee_id, visitor_id, transaction_type, amount):
    return {
        'transaction_id_external': transaction_id,
         'sale_id_external': sale_id if sale_id is not None else "",
        'employee_id_external': employee_id,
        'visitor_id_external': visitor_id,
        'amount': amount,
        'transaction_type': transaction_type,
        'transaction_date': fake.date_this_year(),
    }

