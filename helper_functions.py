# Helper function for shopping app

def sum_products(product_list):
    """ Given a list of products, return the sum of their prices """
    sum = 0
    for product in product_list:
        sum += product.price
    return sum