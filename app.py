"""Shopping cart application."""

from flask import Flask, request, session, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from products import Product                # import Product class
from helper_functions import sum_products   # import helper function to sum up total of purchased products

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretshehe"

debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """Homepage: show list of products with link to product page."""
    product_list = Product.get_all()
    return render_template("homepage.html", products=product_list)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    """Show detail of product, along with add-to-cart form."""
    product_info = Product.get_by_id(product_id)

    return render_template("product.html", product=product_info)

@app.route("/cart")
def show_cart():
    """Show shopping cart."""
    # session['cart'] holds the IDs for purchased products
    # use Product.get_by_id to turn IDs into products
    # then pass along the list of purchased_products to render_template
    purchased_products = [Product.get_by_id(id) for id in session['cart']]
    total_price = sum_products(purchased_products)

    return render_template("cart.html", products=purchased_products, total=total_price)


@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    """ Handle "add to cart" button click by:
    - adding ID of selected product to session['cart'] 
    - redirecting user to homepage (and flash message "product has been added to cart")
    """
    product_id = request.form["product_id"]

    if 'cart' not in session: 
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True

    product_name = Product.get_by_id(product_id).name

    flash(f"{product_name} has been added to your cart") # flash message added to homepage.html
    return redirect("/")

# missing routes:
#   /clear-cart   [in further study]

# 7. Debrief
# Q: What are good design reasons we put all of the stuff about the products in a separate file, rather than in app.py?
# A: We are separating our concerns by creating separate files for products and app.py
#    app.py contains code that handles our Flask app, while products.py contains code that has to do with our Product class.

# Q: We’re only storing the product ID in the session, rather than storing everything you’ll need later, like the product name and price. Why is this better design?
# A: In our Product class we defined a method that only requires the product ID to obtain all the other information about the product
#    As such, we only need the product ID to "unlock" access to the other information we need.
#    By only storing and passing the product ID, we are minimizing the amount of information we need to store and transmit.

# Q: We could have simply exposed a global dictionary, products and had your app.py loop over that and search that directly
#    to get all products or find a product. What’s better about our design, where we use the Product API to do this stuff?
# A: The current design is cleaner. 
#    The Product API handles things related to getting information about products and adding things to the product dictionary.
#    app.py handles all things related to the app (and calls the API to get information to populate the web-app)