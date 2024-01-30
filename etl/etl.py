import mysql.connector
from pymongo import MongoClient
import time


def connect_to_mongo():
    # Create MongoDB client
    return MongoClient("mongodb://mongo:27017/")


def connect_to_mysql(retry_num=5, delay=5):
    # Attempt to create a connection to MySQL with a specified number of retries and delay
    for i in range(retry_num):
        try:
            return mysql.connector.connect(
                host="mysql",
                user="root",
                password="password",
                database="weather"
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL: {e}")
            print(f"Retrying connection in {delay} seconds...")
            time.sleep(delay)
    # If the connection fails, raise an exception
    raise Exception("Failed to connect to MySQL")


def fetch_from_mongo(mongo_collection):
    # Extract the last document from MongoDB
    return mongo_collection.find().sort('_id', -1).limit(1)


def insert_into_mysql(mysql_cursor, name, temp_kelvin):
    # Convert temperature from Kelvin to Celsius
    temp_celsius = temp_kelvin - 273.15

    # Insert data into MySQL
    insert_query = "INSERT INTO weather_data (city, temperature_celsius) VALUES (%s, %s)"
    mysql_cursor.execute(insert_query, (name, temp_celsius))


def main():
    mongo_client = connect_to_mongo()
    mysql_conn = None

    try:
        # Attempt to connect to MySQL
        mysql_conn = connect_to_mysql()
        mongo_db = mongo_client["weather_database"]
        mongo_collection = mongo_db["weather_data"]

        while True:  # Start an infinite loop
            last_record = fetch_from_mongo(mongo_collection)
            with mysql_conn.cursor() as mysql_cursor:
                for record in last_record:
                    name = record.get('name', 'Unknown')
                    temp_kelvin = record['main']['temp'] if 'main' in record and 'temp' in record['main'] else None

                    if temp_kelvin is not None:
                        # Convert temperature from Kelvin to Celsius and insert into MySQL
                        temp_celsius = temp_kelvin - 273.15
                        insert_into_mysql(mysql_cursor, name, temp_celsius)
                        mysql_conn.commit()
                        print(f"Data inserted: {name}, {temp_celsius} °C")
                    else:
                        print("No temperature data found in the record")
            time.sleep(15)  # Pause for 15 seconds
    except KeyboardInterrupt:
        print("Interrupted by the user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connections
        if mysql_conn:
            mysql_conn.close()
        mongo_client.close()


if __name__ == "__main__":
    main()
