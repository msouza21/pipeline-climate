from confluent_kafka import Consumer, KafkaException
from dotenv import load_dotenv
from config.s3_client import s3_client
from config.kafka_config import api_names
import time

cons_delay = 300

load_dotenv()

for api_name in api_names:
    topic = api_name

def upload_s3(file_name, data):
    bucket_name = 's3bucketsz'

    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=data)
        print(f'Uploading {file_name} to S3')
        time.sleep(cons_delay)
    except Exception as e:
        print(f'Error uploading {file_name} to S3: {str(e)}')

def consumer_msg():

    cons_config = {
        'bootstrap.servers': 'broker-1:29092,broker-2:29094',
        'group.id': 's3-consumer',
        'auto.offset.reset': 'earliest'
    }

    cons = Consumer(cons_config)
    cons.subscribe([topic])

    i = 0
    while True:
        try:
            msg = cons.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            data = msg.value()
            ext_s3 = None
            for header in msg.headers():
                if header[0] == 'file_ext':
                    ext_s3 = header[1].decode('utf-8')
                    break

            if not ext_s3:
                ext_s3 = 'data'

            file_name = f'data/{msg.topic()}-{i+1}.{ext_s3}'

            if ext_s3 == 'json':
                data = data.decode('utf-8')

            upload_s3(file_name, data)
            i += 1

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f'Error in upload to S3: {str(e)}')

    cons.close()
