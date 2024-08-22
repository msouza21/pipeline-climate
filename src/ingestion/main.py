import os, json
from manage_data import read_data
from kakfa_prod import produce_msg, prod
from kafka_cons import consumer_msg
from config.kafka_config import api_names

from prefect import task

input_dir = ('../../data/aux')
topic_prefix = 'data-file'



@task
def main():
    while True:
        data = None
        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)

            if file == 'api-config.json':
                print(f'Processing config file: {file}')
                with open(file_path, 'r') as f:
                    config_data = json.load(f)

                for api_name in api_names:
                    if api_name in config_data:
                        config = config_data[api_name]
                        ocult_params = ["appid", "key", "units"]
                        params = [config['params'].get(param, '') for param in config['params'] if param not in ocult_params]
                        data = read_data(api_name, *params)

                continue
            
            if file != 'api-config.json':            
                ext = os.path.splitext(file_path)[1][1:]
                if ext in ['json', 'csv', 'parquet', 'orc', 'txt']:
                    print(f'Processing the file: {file_path}')

                    data = read_data(file_path)
                    if data:
                        produce_msg(topic_prefix + "-" + os.path.basename(file), data, ext)

        if data:
            i = 0
            print(f'Getting data from {api_name} {i+1}x')
            topic = api_name
            produce_msg(topic, data, 'json')
            break
        
        prod.flush()
        
if __name__ == '__main__':
    main()
    consumer_msg()