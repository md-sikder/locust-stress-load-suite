import logging
import time
from locust import HttpUser, events, between
from influxdb_client import InfluxDBClient
from config.config import Config

from tasks import UserBehavior  # Import tasks from tasks.py

# InfluxDB client setup
def save_to_influxdb(request_type, name, response_time, response_length, exception):
    try:
        client = InfluxDBClient(
            url=f"http://{Config.INFLUXDB_HOST}:{Config.INFLUXDB_PORT}",
            token=Config.INFLUXDB_TOKEN
        )
        write_api = client.write_api()

        # Correct Line Protocol Format
        data = f'locust_test,request_type={request_type},name={name} response_time={response_time},response_length={response_length} {int(time.time() * 1e9)}'
        write_api.write(Config.INFLUXDB_BUCKET, Config.INFLUXDB_ORG, data)

        client.close()
    except Exception as e:
        logging.error(f"Failed to write to InfluxDB: {e}")

# Event listener to save results to InfluxDB
@events.request.add_listener
def request_listener(request_type, name, response_time, response_length, exception, **kwargs):
    save_to_influxdb(request_type, name, response_time, response_length, exception)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
