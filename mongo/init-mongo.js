// init-mongo.js

db.createUser({
  user: "admin",
  pwd: "password",
  roles: [
    {
      role: "readWrite",
      db: "weather_database",
    },
  ],
});

db.weather_data.createIndex({ timestamp: 1 });
