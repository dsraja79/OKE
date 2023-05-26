const express = require('express');
const warehouseData = require('./warehouse.json');
const app = express();
const port = 3000;

const db = require("./models");

db.sequelize.sync()
  .then(async () => {
    console.log('Database synced');
    await db.warehouse.destroy({ truncate: true });
    await db.warehouse.bulkCreate(warehouseData);
    console.log('Warehouse data loaded successfully');
  })
  .catch(error => {
    console.error('Error syncing database:', error);
  });

app.get('/api/warehouse', async (req, res) => {
  try {
    const warehouseList  = await db.warehouse.findAll();
    res.json(warehouseList );
  } catch (error) {
    console.error('Error fetching warehouse data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

//Get Warehouse data for a product
app.get('/api/warehouse/:product', async (req, res) => {
  const product = req.params.product;

  try {
    const warehouseList = await db.warehouse.findAll({
      where: {
        product: product
      }
    });

    res.json(warehouseList);
  } catch (error) {
    console.error('Error fetching warehouse data:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.listen(port, () => {
  console.log(`Warehouse Service is listening on port ${port}`);
});