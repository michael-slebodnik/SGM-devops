CREATE TABLE weather_data (
    city VARCHAR(255),
    temperature FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- database/account for metabase container access
create database metabase;
CREATE USER metabase@'%' IDENTIFIED BY 'metabasedatabasepassword';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, INDEX, DROP, ALTER, CREATE TEMPORARY TABLES, LOCK TABLES ON metabase.* TO metabase@'%';
