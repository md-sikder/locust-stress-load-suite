import logging
from datetime import datetime

# from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient

from config.config import Config

def save_to_influxdb(request_type, name, response_time, response_length, exception):
    client = InfluxDBClient(host=Config.INFLUXDB_HOST, port=Config.INFLUXDB_PORT)
    client.switch_database(Config.INFLUXDB_DBNAME)
    json_body = [{
        "measurement": "performance_test",
        "time": datetime.utcnow().isoformat(),
        "fields": {
            "request_type": request_type,
            "name": name,
            "response_time": response_time,
            "response_length": response_length,
            "exception": str(exception) if exception else "None"
        }
    }]
    client.write_points(json_body)
