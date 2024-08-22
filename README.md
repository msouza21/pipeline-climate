# Pipeline-Climate
## Overview
This are a learning initiative aimed at developing data engineering skills. This project involves utilizing APIs to request climate-related data and testing the workflow and infrastructure. The architecture leverages various tools within Docker containers, including:

Prefect used as orquestration pipeline
Apache Kafka as broker of data
AWS S3 as the temporary data lake
Apache Spark to processing the data
PostgreSQL as the primary database

## Project Settings

The project structure is organized as follows:

- BGD-Project
    - └── pipeline-climate
        -    ├── compose 
        -    ├── config   
        -    ├── data   
        -    ├── ignore   
        -    ├── src 
        -    ├── Some others files
   

Where the purpose of each folder is:

compose: With folders composes each service in container (kafka, spark, postgres)

config: Being the setup config services in python

data: With folders /aux and /help to auxiliary the setup

ignore: Folder to ignore some files like  /jars for jars files trought .gitignore

src: Folder with layers of scripts (ingestion, orquestration, process and store), having too /znotebooks for explore and /test for testing

It is essential to configure the volumes and other options to match your local environment. The provided docker-compose.yml files are examples and should be modified to fit your specific project needs.

## Objectives

The primary goal of this project is to develop a system for collecting data on various climate-related topics to provide insights, such as:
    Weather conditions
    Air and water quality
    Geospatial data

This system will facilitate the monitoring and evaluation of climate conditions across different regions in world, where the principal data font is weather.

## How to Run

Follow these steps to set up and run the project:

Clone the repository:

```git clone https://github.com/msouza21/pipeline-climate```

Install Docker and Docker Compose on your machine.

Adjust the configurations in the docker-compose.yml files and other tools like python as necessary.
It's recommended to create a venv and install the libs from file requirements.txt in her, following the below instructions.

```python3 -m venv name``` 

Where in 'name' is the wanted name to venv, later for active the venv:

Linux/macOS

``` source venv/bin/activate```

Windows

```$ venv\Scripts\activate```

For install the libs run the command:

```pip install -r requeriments.txt```

Later you can run the deployment script to up the containers:

```python3 deploy-dck.py```

Coming back to /src/orquestration, for automate the process using Prefect:

```python3 pipe_flow.py```

## More details

For don't be a heavy project, download the jars files trought maeven repository and setup in /ignore/jars

For a detailed overview of the project's architecture, development phases, challenges faced, and more, can be posted a Medium article that will a better understanding
of project in general.

Having a cli-help.txt file to some actions in command line if necessary/wanted, but not mandatory to sucefull execution project.

## License

This project is builded in MIT license.  See [LICENSE](https://github.com/msouza21/pipeline-climate/blob/main/LICENSE) for more information.
