import csv, os, json
from io import BytesIO, StringIO
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.orc as orc
from ingestion.api import read_json_data
from config.kafka_config import api_configs

#For others types of data, functions personalized to these, like CSV,Parquet and others
def read_csv_data(file_path):
    with open(file_path, 'r') as file:
        data = csv.reader(file)
        return data

def read_parquet_data(file_path):
    table = pq.read_table(file_path)
    return table

def read_orc_data(file_path):
    table = orc.ORCFile(file_path).read()
    return table

def read_txt_data(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()


def read_data(source, *args):
    #Identify the type of data by the final
    if source in api_configs:
        return read_json_data(source, *args)

    ext = os.path.splitext(source)[-1].lower()
    format_file = {
        '.json': read_json_data,
        '.csv': read_csv_data,
        '.parquet': read_parquet_data,
        '.orc': read_orc_data,
        '.txt': read_txt_data
    }

    if ext in format_file:
        return format_file[ext](source)
    else:
        return ValueError(f"Invalid format {ext} not supported")
    
def write_data(format, data):
    buffer = BytesIO()

    if format == 'json':
        buffer = StringIO()
        json.dump(data, buffer)
        return buffer.getvalue()
    
    elif format == 'csv':
        writer = csv.writer(buffer)
        writer.writerows(data)
        return buffer.getvalue()
    
    elif format == 'parquet':
        if isinstance(data, pa.Table):
            pq.write_table(data, buffer)
        else:
            raise ValueError('Error instance format file')
        return buffer.getvalue()
    
    elif format == 'orc':
        if isinstance(data, pa.Table):
            orc.write_table(data, buffer)
        else:
            raise ValueError('Error instance format file')
        return buffer.getvalue()
    
    elif format == 'txt':
        buffer.write(data.encode('utf-8'))
        return buffer.getvalue()
    else:
        raise ValueError(f"Invalid format {format} not supported")