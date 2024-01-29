import mysql.connector
from pymongo import MongoClient
import time


def connect_to_mongo():
    # Создание клиента MongoDB
    return MongoClient("mongodb://mongo:27017/")


def connect_to_mysql(retry_num=5, delay=5):
    # Попытка создания подключения к MySQL с заданным количеством повторов и задержкой
    for i in range(retry_num):
        try:
            return mysql.connector.connect(
                host="mysql",
                user="root",
                password="password",
                database="weather"
            )
        except mysql.connector.Error as e:
            print(f"Ошибка подключения к MySQL: {e}")
            print(f"Повторное подключение через {delay} секунд(ы)...")
            time.sleep(delay)
    # Если подключение не удалось, выбросить исключение
    raise Exception("Не удалось подключиться к MySQL")


def fetch_from_mongo(mongo_collection):
    # Извлечение последнего документа из MongoDB
    return mongo_collection.find().sort('_id', -1).limit(1)


def insert_into_mysql(mysql_cursor, name, temp):
    # Вставка данных в MySQL
    insert_query = "INSERT INTO weather_data (city, temperature) VALUES (%s, %s)"
    mysql_cursor.execute(insert_query, (name, temp))


def main():
    mongo_client = connect_to_mongo()
    mysql_conn = None

    try:
        # Попытка подключения к MySQL
        mysql_conn = connect_to_mysql()
        mongo_db = mongo_client["weather_database"]
        mongo_collection = mongo_db["weather_data"]

        while True:  # Начало бесконечного цикла
            last_record = fetch_from_mongo(mongo_collection)
            with mysql_conn.cursor() as mysql_cursor:
                for record in last_record:
                    name = record.get('name', 'Unknown')
                    temp = record['main']['temp'] if 'main' in record and 'temp' in record['main'] else None

                    if temp is not None:
                        insert_into_mysql(mysql_cursor, name, temp)
                        mysql_conn.commit()
                        print(f"Data inserted: {name}, {temp}")
                    else:
                        print("No temperature data found in the record")
            time.sleep(15)  # Пауза в 15 секунд
    except KeyboardInterrupt:
        print("Interrupted by the user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Закрытие подключений
        if mysql_conn:
            mysql_conn.close()
        mongo_client.close()


if __name__ == "__main__":
    main()
