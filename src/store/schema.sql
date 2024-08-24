-- Active: 1722192827086@@localhost@5455
CREATE TABLE IF NOT EXISTS openweather_data (
    name VARCHAR(50) NOT NULL,
    lat  FLOAT,
    lon  FLOAT,
    humidity INT,
    pressure INT,
    temp_celsius FLOAT,
    country VARCHAR(50) NOT NULL,
    wind_speed FLOAT,
    wind_deg INT,
    weather_main VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS weatherapi_data (
    name VARCHAR(50) NOT NULL,
    lat  FLOAT,
    lon  FLOAT,
    temp FLOAT,
    humidity INT,
    pressure INT,
    temp_celsius FLOAT,
    country VARCHAR(50) NOT NULL,
    wind_speed FLOAT,
    wind_deg INT,
    weather_main VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS weatherbit_data (
    name VARCHAR(50) NOT NULL,
    lat  FLOAT,
    lon  FLOAT,
    temp FLOAT,
    humidity INT,
    pressure INT,
    temp_celsius FLOAT,
    country VARCHAR(50) NOT NULL,
    wind_speed FLOAT,
    wind_deg INT,
    weather_main VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS openaq_data (
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    lat FLOAT,
    lon FLOAT,
    pm25 FLOAT,
    pm10 FLOAT,
    no2 FLOAT,
    so2 FLOAT,
    o3 FLOAT
);

CREATE TABLE IF NOT EXISTS bigdata_cloud_data (
    city VARCHAR(50) NOT NULL,
    lat FLOAT,
    lon FLOAT,
    subdivision VARCHAR(50),
    country VARCHAR(50),
    continent VARCHAR(50),
    continent_code VARCHAR(50)
);