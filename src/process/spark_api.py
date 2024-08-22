from config.spark_config import spark
from pyspark.sql.functions import col, explode
import logging

data_dir = "s3a://s3bucketsz/data/"

def process_json(spark, json_file):
    try:
        df = spark.read.json(data_dir + json_file, multiline=True)
        api_name = json_file.split('-')[0]
        return df, api_name
    except Exception as e:
        logging.error(f"Error processing JSON file`{json_file}: {e}")
        return None, None

def process_api(df, api_name):
    if api_name == "openweather":

        return df \
            .withColumn("lat", col("coord.lat")) \
            .withColumn("lon", col("coord.lon")) \
            .withColumn("name", col("name")) \
            .withColumn("pressure", col("main.pressure")) \
            .withColumn("humidity", col("main.humidity")) \
            .withColumn("temp_celsius", col("main.temp")) \
            .withColumn("country", col("sys.country")) \
            .withColumn("wind_speed", col("wind.speed")) \
            .withColumn("wind_deg", col("wind.deg")) \
            .withColumn("weather_main", col("weather.main")) \
            .drop("coord", "main", "sys", "weather", "wind", "dt", 
                "description", "icon", "id", "base", "temp_min", 
                "temp_max", "sea_level", "grnd_level", "visibility", 
                "clouds", "type", "sunrise", "sunset", "timezone", "cod")
    
    elif api_name == 'weather_api':
        return df \
            .withColumn("name", col("location.name")) \
            .withColumn("country", col("location.country")) \
            .withColumn("lat", col("location.lat")) \
            .withColumn("lon", col("location.lon")) \
            .withColumn("temp_celsius", col("current.temp_c")) \
            .withColumn("wind_speed", col("wind_mph")) \
            .withColumn("wind_deg", col("wind_degree")) \
            .withColumn("pressure", col("pressure_mb")) \
            .withColumn("humidity", col("humidity")) \
            .withColumn("weather_main", col("condition.text")) \
            .drop("region", "tz_id", "localtime_epoch", "localtime", "current"
                "last_updated_epoch", "last_updated", "temp_f", "is_day", "condition", 
                "icon", "code", "wind_mph", "wind_kph", "wind_dir", "pressure_in",
                "precip_mm", "precip_in", "cloud", "feelslike_c", "feelslike_f",
                "windchill_c", "windchill_f", "heatindex_c", "heatindex_f", "dewpoint_c",
                "dewpoint_f", "vis_km", "vis_miles", "uv", "gust_mph", "gust_kph")
    
    elif api_name == 'weatherbit':
        return df \
            .withColumn("lat", col("data.lat")) \
            .withColumn("lon", col("data.lon")) \
            .withColumn("name", col("data.city_name")) \
            .withColumn("temp_celsius", col("data.app_temp")) \
            .withColumn("pressure", col("data.pres")) \
            .withColumn("humidity", col("data.rh")) \
            .withColumn("country", col("data.country_code")) \
            .withColumn("wind_speed", col("data.wind_spd")) \
            .withColumn("wind_deg", col("data.wind_dir")) \
            .withColumn("weather_main", col("data.weather.description")) \
            .drop("data.clouds", "data.datetime", "data.dewpt", "data.dhi", 
                  "data.dni", "data.elev_angle", "data.ghi", "data.gust", 
                  "data.h_angle", "data.ob_time", "data.pod", "data.precip", 
                  "data.slp", "data.snow", "data.solar_rad", "data.sources", 
                  "data.state_code", "data.station", "data.sunrise", 
                  "data.sunset", "data.timezone", "data.ts", "data.uv", 
                  "data.vis")

    elif api_name == 'openaq':
        # Process OpenAQ data
        return df \
            .withColumn("city", col("city")) \
            .withColumn("country", col("country")) \
            .withColumn("lat", col("coordinates.latitude")) \
            .withColumn("lon", col("coordinates.longitude")) \
            .withColumn("pm25", col("parameters[0].lastValue")) \
            .withColumn("pm10", col("parameters[1].lastValue")) \
            .withColumn("no2", col("parameters[2].lastValue")) \
            .withColumn("so2", col("parameters[3].lastValue")) \
            .withColumn("o3", col("parameters[4].lastValue")) \
            .drop("parameters", "coordinates")

    elif api_name == 'bigdata_cloud':
        return df \
            .withColumn("lat", col("latitude")) \
            .withColumn("lon", col("longitude")) \
            .withColumn("country", col("countryName")) \
            .withColumn("city", col("city")) \
            .withColumn("subdivision", col("principalSubdivision")) \
            .withColumn("continent", col("continent")) \
            .withColumn("continent_code", col("continentCode")) \
            .drop("lookupSource", "localityLanguageRequested", "locality", 
                  "localityInfo", "postcode", "plus_code")
    
    else:
        logging.error(f"Unsupported API: {api_name}")
        return None