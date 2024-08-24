import sys, os, logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from config.spark_config import spark, db_url, db_properties
from process.spark_api import process_json, process_api
from process.data_manage import insert_postgres, list_json
from config.s3_client import create_client, s3_bucket, s3_prefix
from datetime import datetime, timezone, timedelta

from prefect import task

@task
def main():

    s3 = create_client()
    
    utc_3 = timezone(timedelta(hours=-3))
    last_processed = datetime.now(utc_3) - timedelta(minutes=50)
    logging.info(f"Processing files modified after: {last_processed}")

    json_files = list_json(s3, s3_bucket, s3_prefix, last_processed)

    for file in json_files:
        logging.info(f"Processing file: {file}")

        df, api_name = process_json(spark, file)

        if df and api_name:
            df_processed = process_api(df, api_name)

            if df_processed:
                insert_postgres(df_processed, api_name, db_url, db_properties)
            else:
                logging.info("Failed to process dataframe")
        else:
            logging.error("Failed to process JSON file")
    spark.stop()

if __name__ ==  "__main__":
    main()