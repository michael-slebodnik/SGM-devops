
# etl_process.py
# ETL Process - Fetch data from MongoDB and prepare for MySQL

import pymongo
import mysql.connector

# Connect to MongoDB
mongo_client = pymongo.MongoClient('mongodb://mongo:27017/')
mongo_db = mongo_client.weather_database
mongo_collection = mongo_db.weather_data

# Connect to MySQL
mysql_db = mysql.connector.connect(
    host="mysql",
    user="user",
    password="password",
    database="mydatabase"
)
mysql_cursor = mysql_db.cursor()

# ETL Process
try:
    # Fetch data from MongoDB
    mongo_data = mongo_collection.find()

    for data in mongo_data:
        # Transform data if needed
        transformed_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            # Add more transformations as needed
        }

        # Load data into MySQL
        mysql_cursor.execute(
            "INSERT INTO weather_data (temperature, humidity) VALUES (%s, %s)",
            (transformed_data["temperature"], transformed_data["humidity"])
        )
        mysql_db.commit()

    print("ETL Process completed successfully.")

except Exception as e:
    print(f"Error in ETL Process: {e}")

finally:
    # Close connections
    mysql_cursor.close()
    mysql_db.close()
    mongo_client.close()
