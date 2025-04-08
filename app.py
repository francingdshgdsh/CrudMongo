from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from product import Product

db = dbase.dbConnection()

app = Flask(__name__)

# ruta principal
@app.route('/')
def home():
    products = db['products']
    productsRecived = list(products.find())
    return render_template('index.html', products=productsRecived)

#ruta buscar
@app.route('/search')
def search():
    query = request.args.get('query')
    products = db['products']

    search_filter = {
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"price": {"$regex": query, "$options": "i"}},
            {"quantity": {"$regex": query, "$options": "i"}},
            {"category": {"$regex": query, "$options": "i"}},
            {"location": {"$regex": query, "$options": "i"}}
        ]
    }

    results = list(products.find(search_filter))
    all_products = list(products.find())

    return render_template('index.html', products=all_products, search_results=results)


# metodo agregar
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']
    location = request.form['location']

    if name and price and quantity and category and location:
        product = Product(name, price, quantity, category, location)
        products.insert_one(product.toDBCollection())
        return redirect(url_for('home'))
    else:
        return notFound()

# metodo delete
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

# eliminar todo
@app.route('/delete_all', methods=['POST'])
def delete_all():
    products = db['products']
    products.delete_many({})  
    return redirect(url_for('home'))

# metodo editar
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    category = request.form['category']
    location = request.form['location']

    if name and price and quantity and category and location:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity, 'category': category, 'location': location}})
        return redirect(url_for('home'))
    else:
        return notFound()

# error
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'no encontrado ' + request.url,
        'status': '404 not found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

#editar tabla
@app.route('/update_field', methods=['POST'])
def update_field():
    old_field = request.form['old_field']
    new_field = request.form['new_field']
    
    if old_field and new_field:
        products = db['products']
        documents = products.find({old_field: {"$exists": True}})
        
        for doc in documents:
            products.update_one({'_id': doc['_id']}, {
                '$set': {new_field: doc[old_field]},
                '$unset': {old_field: ""}
            })

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=4000)