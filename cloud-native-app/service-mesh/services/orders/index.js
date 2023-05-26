// Import required modules
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const axios = require('axios');
require('dotenv').config();


// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(error => console.error('Failed to connect to MongoDB', error));

// Define Order schema
const orderSchema = new mongoose.Schema({
  customerName: String,
  product: String,
  price: Number,
  quantity: Number,
});

// Create Order model
const Order = mongoose.model('Order', orderSchema);

// Create Express app
const app = express();

// Middleware for parsing JSON data
app.use(bodyParser.json());

// Create an order
app.post('/api/orders', (req, res) => {
  const { customerName, product, quantity } = req.body;
  
  console.log(`product service url is: ${process.env.PRODUCTS_API_URL}${product}`);

  // Fetch the price from the product service
  axios.get(`${process.env.PRODUCTS_API_URL}${product}`)
    .then(response => {
      const price = response.data.price;

      // Create a new Order instance
      const order = new Order({
        customerName,
        product,
        price,
        quantity,
      });

      // Save the order to the database
      return order.save();
    })
    .then(order => res.status(201).json(order))
    .catch(error => res.status(500).json({ error: 'Failed to create order' }));
});

// Retrieve all orders
app.get('/api/orders', (req, res) => {
  Order.find()
    .then(orders => res.json(orders))
    .catch(error => res.status(500).json({ error: 'Failed to retrieve orders' }));
});




// Start the server
app.listen(3000, () => {
  console.log('Order Service started on port 3000');
});
