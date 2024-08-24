import os, json,time, threading
from ingestion.manage_data import read_data
from ingestion.kakfa_prod import produce_msg, prod
from ingestion.kafka_cons import consumer_msg
from config.kafka_config import api_names
from prefect import task

topic_prefix = "data-file"
input_dir = ('../../data/aux')

@task
def prod_loop(api_name):
    while True:
        data = None
        for file in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file)

            if file == 'api-config.json':
                with open(file_path, 'r') as f:
                    config_data = json.load(f)

                if api_name in config_data:
                    config = config_data[api_name]
                    ocult_params = ["appid", "key", "units"]
                    params = [config['params'].get(param, '') for param in config['params'] if param not in ocult_params]
                    data = read_data(api_name, *params)

                    if data:
                        print(f'Getting data from {api_name}')
                        produce_msg(api_name, data, 'json')
                continue

            if file != 'api-config.json':            
                ext = os.path.splitext(file_path)[1][1:]
                if ext in ['json', 'csv', 'parquet', 'orc', 'txt']:
                    print(f'Processing the file: {file_path}')

                    data = read_data(file_path)
                    if data:
                        produce_msg(topic_prefix + "-" + os.path.basename(file), data, ext)

        if data:
            produce_msg(api_name, data, 'json')

        prod.flush()
        #time.sleep(5)

def main():
    prod_threads = []
    cons_threads = []

    for api_name in api_names:
        # Create a producer thread for each API
        prod_thread = threading.Thread(target=prod_loop, args=(api_name,))
        prod_threads.append(prod_thread)
        prod_thread.start()

        # Create a consumer thread for each API
        cons_thread = threading.Thread(target=consumer_msg, args=(api_name,))
        cons_threads.append(cons_thread)
        cons_thread.start()

    # Join threads
    for thread in prod_threads:
        thread.join()

    for thread in cons_threads:
        thread.join()

if __name__ == '__main__':
    main()