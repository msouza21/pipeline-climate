import os,json
from dotenv import load_dotenv
from confluent_kafka.admin import AdminClient

load_dotenv("../../ignore/.env")

config_path = ('../../data/aux/api-config.json')

with open(config_path) as config_file:
    api_configs = json.load(config_file)


api_keys ={
    "openweather": os.getenv("OPENWEATHER_API_KEY", ""),
    "weatherapi": os.getenv("WEATHERAPI_API_KEY", ""),
    "weatherbit": os.getenv("WEATHERBIT_API_KEY", ""),
    "openaq": os.getenv("OPENAQ_API_KEY", ""),
    "bigdata": os.getenv("BIGDATA_API_KEY", ""),
}

param_info = {
    'q': 'location'
}

api_names = ['openweather']

admin_client = AdminClient({'bootstrap.servers': 'broker-1:29092,broker-2:29094'})

message_count = 0
msg_limit = 50


def create_partitions(topic, partition_count):
    fs = admin_client.alter_partitions([{
        'topic':topic,
        'new_count': partition_count
    }])
    for topic, f in fs.items():
        try:
            f.result()
            print(f'Partitions from topic: {topic} increased to: {partition_count}.')
        except Exception as e:
            print(f'Error in alter partitions from topic {topic}: {str(e)}.')

def get_partitions(topic):
    topic_metadata = admin_client.list_topics(topic)
    if topic_metadata.topics.get(topic):
        return len(topic_metadata.topics[topic].partitions)
    return 0
