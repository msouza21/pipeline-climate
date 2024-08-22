#Using the command ip addr show to find the ip for connect to master spark
import sys
sys.path.append('/config')

from pyspark.sql import SparkSession
from config.s3_client import aws_creds

jars = "../../ignore/jars"

spark = SparkSession.builder \
    .appName("Spark-Process") \
    .master("spark://172.17.0.1:7077") \
    .config("spark.jars", ",".join([
        f"{jars}/hadoop-aws-3.3.1.jar",
        f"{jars}/aws-java-sdk-bundle-1.11.901.jar",
        f"{jars}/postgresql-42.7.3.jar"
    ])) \
    .getOrCreate()

spark.sparkContext.setLogLevel("DEBUG")


hadoopConf = spark._jsc.hadoopConfiguration()
hadoopConf.set("fs.s3a.access.key",aws_creds["AWS_ACCESS_KEY_ID"])
hadoopConf.set("fs.s3a.secret.key",aws_creds["AWS_SECRET_ACCESS_KEY"])
hadoopConf.set("f3.s3a.endpoint", f"s3.{aws_creds['AWS_REGION_BUCKET']}.amazonaws.com")

db_url = "jdbc:postgresql://postgres:5455/pgcli" #Url to connect the db of compose

db_properties = {
    "user": "pgcli",
    "password": "pgcli12",
    "driver": "org.postgresql.Driver"    
}

