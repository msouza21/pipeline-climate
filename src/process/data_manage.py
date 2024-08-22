import logging
import psycopg2


def list_json(s3, s3_bucket, s3_prefix, last_processed):
    response = s3.list_objects_v2(Bucket=s3_bucket, Prefix=s3_prefix)
    files = [
        content['key'] for content in response.get('Contents', [])
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

        conn = psycopg2.connect(db_url, **db_properties)
        cur = conn.cursor()

        for row in df.collect():
            values =  tuple(row[col] for col in columns)
            cur.execute(insert_sql, values)

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error inserting data to postgres: {e}")