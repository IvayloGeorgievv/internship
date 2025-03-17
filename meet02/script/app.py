from flask import Flask

from routes.visitors import visitors_bp
from routes.tickets import tickets_bp
from routes.attractions import attractions_bp
from routes.employees import employees_bp
from routes.establishments import establishments_bp
from routes.products import products_bp
from routes.promotions import promotions_bp
from routes.roles import roles_bp
from routes.sales import sales_bp
from routes.transactions import transactions_bp
app = Flask(__name__)

app.register_blueprint(visitors_bp, url_prefix='/visitors')
app.register_blueprint(tickets_bp, url_prefix='/tickets')
app.register_blueprint(attractions_bp, url_prefix='/attractions')
app.register_blueprint(employees_bp, url_prefix='/employees')
app.register_blueprint(establishments_bp, url_prefix='/establishments')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(promotions_bp, url_prefix='/promotions')
app.register_blueprint(roles_bp, url_prefix='/roles')
app.register_blueprint(sales_bp, url_prefix='/sales')
app.register_blueprint(transactions_bp, url_prefix='/financial')

if __name__ == '__main__':
    app.run()
