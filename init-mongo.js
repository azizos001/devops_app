db = db.getSiblingDB('ecommerce');

// Create collections with validation
db.createCollection('products', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'price', 'description', 'category'],
      properties: {
        name: { bsonType: 'string' },
        price: { bsonType: 'number', minimum: 0 },
        description: { bsonType: 'string' },
        category: { bsonType: 'string' },
        image: { bsonType: 'string' }
      }
    }
  }
});

db.createCollection('stock', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['product_id', 'quantity'],
      properties: {
        product_id: { bsonType: 'string' },
        quantity: { bsonType: 'int', minimum: 0 }
      }
    }
  }
});

db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'email'],
      properties: {
        user_id: { bsonType: 'string' },
        email: { bsonType: 'string' },
        name: { bsonType: 'string' },
        address: { bsonType: 'string' },
        phone: { bsonType: 'string' },
        created_at: { bsonType: 'date' },
        updated_at: { bsonType: 'date' }
      }
    }
  }
});

db.createCollection('orders', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['user_id', 'items', 'total_amount', 'status', 'created_at'],
      properties: {
        user_id: { bsonType: 'string' },
        items: { 
          bsonType: 'array',
          items: {
            bsonType: 'object',
            required: ['product_id', 'quantity', 'price'],
            properties: {
              product_id: { bsonType: 'string' },
              quantity: { bsonType: 'int', minimum: 1 },
              price: { bsonType: 'number', minimum: 0 }
            }
          }
        },
        total_amount: { bsonType: 'number', minimum: 0 },
        shipping_address: { bsonType: 'string' },
        status: { 
          enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'] 
        },
        created_at: { bsonType: 'date' }
      }
    }
  }
});

// Create indexes
db.products.createIndex({ category: 1 });
db.stock.createIndex({ product_id: 1 }, { unique: true });
db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });
db.orders.createIndex({ user_id: 1 });
db.orders.createIndex({ created_at: 1 });