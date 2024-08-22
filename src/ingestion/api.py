#Config APIs
import requests, sys
sys.path.append('../../')
import config
from config.kafka_config import api_configs, api_keys

for api_name, config in  api_configs.items():
    if api_name in api_keys:
        config["params"]["key"] = api_keys[api_name]

#Reading data json from APIs
def read_json_data(api_name, *args):
    """Request of data based in wanted API"""
    if api_name in api_configs:
        config = api_configs[api_name]
        
        params = config["params"].copy()
        params_keys = list(params.keys())

        if api_name in api_keys:
            if 'appid' in params:
                params['appid'] = api_keys[api_name]
            else:
                params['key'] = api_keys[api_name]
        
        for i, key in enumerate(params_keys):
            if i < len(args):
                params[key] = args[i]

        response = requests.get(config["url"], params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error to request data from API: {api_name}: {response.status_code}")
            print(response.text)
    else:
        print(f"API '{api_name}' not found")
        return None