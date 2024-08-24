import os
import json
import time

with open('../ignore/config.json') as config_file:
    config = json.load(config_file)
    compose_dir = config.get("BASE_DIR").rstrip('/')

services = ["kafka", "spark", "postgres"]

def deploy_services():
    for service in services:
        service_dir = os.path.join(compose_dir + "/compose", service)
        compose_file = os.path.join(service_dir, 'docker-compose.yml')
        print(f"Checking {service} compose")
        
        if os.path.exists(compose_file):
            print(f"Deploying {service}...")
            os.chdir(service_dir)
            os.system('docker-compose up -d')
            print('Waiting 30 seconds for next compose')
            time.sleep(30)
            print("Deployment completed")
        else:
            print(f"Compose file not found for {service} at {compose_file}")
    time.sleep(5)
    os.system('clear')

if __name__ == "__main__":
    deploy_services()
