import requests

from datetime import datetime
from flask import Flask, redirect, render_template, Response, request, url_for
from config import Config
app = Flask(__name__)

app.config.from_object(Config)

#Deafult inventory list
inventory_list = [
    {
        'product': 'PRD-01',
        'quantity': 5
    },
    {
        'product': 'PRD-02',
        'quantity': 15
    },
    {
        'product': 'PRD-03',
        'quantity': 7
    }
] 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/reference/")
def reference():
    return render_template("reference.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/order/', methods=['GET', 'POST'])
def create_order(): 
    #Submit Order route      
    if request.method == 'POST':
        # Retrieve the order data from the form
        customerName = request.form['customerName']
        product = request.form['product']
        quantity = request.form['quantity']
        
        print("Calling - Order service")
        order_data = {
            'customerName': customerName,
            'product': product,
            'quantity': quantity
        }
        #create order
        orders_api_url = app.config['ORDERS_API_URL']
        res = requests.post(orders_api_url, json=order_data)
        
        if res.status_code == 201:
            # Order created successfully
            print("Order created successfully!!!")
        else:
            # Failed to create order, handle the error here
            print("Error creating order!!!")

        return redirect(url_for('get_orders'))
    
    #Create Order Page - Show inventory and order form
    try:
        #Make API call to retrieve inventory data
        inventory_api_url = app.config['INVENTORY_API_URL']
        res = requests.get(inventory_api_url)
            
        #Check if API call was successful
        if res.status_code == 200:
            try:
                inventory_list = res.json()            
            except ValueError:
                print("Error: Invalid JSON response")
        else:
            print(f"Error: API call failed with status code {res.status_code}")    
    except ConnectionError as e:
       print("Connection Error:", str(e))
    
    return render_template('order.html', inventory=inventory_list)

@app.route('/inventory', methods=['GET'])
def inventory():
    print("Calling - inventory service")    
    try:
        inventory_api_url = app.config['INVENTORY_API_URL']
        res = requests.get(inventory_api_url)        
        #Check if API call was successful
        if res.status_code == 200:
            try:
                inventory_list = res.json()            
            except ValueError:
                print("Error: Invalid JSON response")
        else:
            print(f"Error: API call failed with status code {res.status_code}")          
    except ConnectionError as e:
       print("Connection Error:", str(e))
    return render_template('inventory.html', inventory=inventory_list)



@app.route('/orders/list', methods=['GET'])
def get_orders():
    print("Calling - Order service")
    orders_api_url = app.config['ORDERS_API_URL']
    res = requests.get(orders_api_url)
    orders = res.json()
    print("web-app:got some orders!")
    return render_template('order_details.html', orders=orders)