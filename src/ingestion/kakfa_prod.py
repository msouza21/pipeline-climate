from confluent_kafka import Producer
from config.kafka_config import msg_limit, message_count, get_partitions, create_partitions
from ingestion.manage_data import write_data
#Kafka config complete

prod_conf = {
    'bootstrap.servers': 'localhost:9092,localhost:9094',
    'client.id': 'py-producer'
}

prod = Producer(**prod_conf) 

def msg_report(err, msg):
    if err is not None:
        print(f'Msg error: {msg} - {err}')
    else:
        print(f'Msg delivered to topic: {msg.topic()}, partition: [{msg.partition()}]')

#Code execution
def produce_msg(topic, data, format):
    global message_count

    prod_data = write_data(format, data)

    if format == 'json':
        file_ext = 'json'
    elif format == 'csv':
        file_ext = 'csv'
    elif format == 'txt':
        file_ext = 'txt'
    else:
        file_ext = 'data' 

    try:      
        prod.produce(topic, key='data', value = prod_data, headers=[('file_ext', file_ext)])
        prod.poll(0)
        message_count += 1

        if message_count >= msg_limit:
            current = get_partitions(topic)
            create_partitions(topic, current + 1)
            message_count = 0

    except Exception as e:
        print(f'Error producing message: {str(e)}')