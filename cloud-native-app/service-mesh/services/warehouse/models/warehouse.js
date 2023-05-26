
module.exports = (sequelize, Sequelize) => {
    const Warehouses = sequelize.define("Warehouses", {
      product: {
        type: Sequelize.STRING
      },
      warehouse: {
        type: Sequelize.STRING
      },
      location: {
        type: Sequelize.STRING
      }      
    });
  
    return Warehouses;
  };