import logging
import psycopg2


def list_json(s3, s3_bucket, s3_prefix, last_processed):
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)
    files = [
        content['Key'] for content in response.get('Contents', [])
        if content['LastModified'] > last_processed
    ]
    return files

def insert_postgres(df, api_name, db_url, db_properties):
    table_name = f"{api_name}_data"
    try:
        columns = df.columns
        columns_str = ', '.join(columns)

        place_holders = ', '.join(["%s"] * len(columns))

        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({place_holders})"

        db_info = db_url.replace("jdbc:postgresql://", "").split("/")
        host_port = db_info[0]
        dbname = db_info[1]

        conn_params = {
            "host": host_port.split(":")[0],
            "port": host_port.split(":")[1],
            "dbname": dbname,
            "user": db_properties["user"],
            "password": db_properties["password"]
        }

        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()
        for row in df.collect():
            values =  tuple(row[col] for col in columns)
            cur.execute(insert_sql, values)

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting data to postgres: {e}")