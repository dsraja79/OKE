const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const axios = require('axios');
require('dotenv').config();

// Define the Inventory schema
const inventorySchema = new mongoose.Schema({
  product: String,
  warehouse: String,
  location: String,
  quantity: Number
});

// Create the Inventory model
const Inventory = mongoose.model('Inventory', inventorySchema);

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URL, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Connected to MongoDB'))
  .catch(error => console.error('Failed to connect to MongoDB', error));


// Load inventory data from inventory.json
const inventoryData = JSON.parse(fs.readFileSync('inventory.json'));

console.log('Loading inventory data...');

// Update or insert inventory data
Promise.all(
  inventoryData.map(async (item) => {
    try {
      const filter = { product: item.product };
      const update = { quantity: item.quantity };

      await Inventory.updateOne(filter, update, { upsert: true });

      console.log(`Updated/Inserted inventory for product: ${item.product}`);
    } catch (err) {
      console.error(`Error updating/inserting inventory for product: ${item.product}`, err);
    }
  })
)
  .then(() => {
    console.log('Inventory data loaded successfully');
  })
  .catch((err) => {
    console.error('Error loading inventory data:', err);
  });


// Create the Express app
const app = express();

app.get('/api/inventory', async (req, res) => {
  try {    
    const inventory = await Inventory.find({});
    const warehouseResponse = await axios.get(`${process.env.WAREHOUSE_API_URL}/api/warehouse`);
    const warehouseData = warehouseResponse.data;

    const inventoryWithWarehouse = inventory.map((item) => {
      const warehouseItem = warehouseData.find((warehouse) => warehouse.product === item.product);
      const warehouseName = warehouseItem ? warehouseItem.warehouse : 'N/A';
      const warehouseLocation = warehouseItem ? warehouseItem.location : 'N/A';

      return {
        product: item.product,
        warehouse: warehouseName,
        location: warehouseLocation,
        quantity: item.quantity,
      };
    });
    console.log('Get all inventory documents -->'+inventoryWithWarehouse);
    res.json(inventoryWithWarehouse);
  } catch (err) {
    console.error('Error:', err);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


// Start the server
app.listen(3000, () => {
  console.log('Inventory service started on port 3000');
});
