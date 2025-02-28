import logging
import os
import time
from locust import HttpUser, events, between
from influxdb_client import InfluxDBClient
from config.config import Config
from tasks import UserBehavior

# Ensure 'logs' directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging (for better debugging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/locust_test.log"),  # Save logs to file
        logging.StreamHandler()  # Print logs to console
    ]
)

# InfluxDB client setup
client = InfluxDBClient(
    url=f"http://{Config.INFLUXDB_HOST}:{Config.INFLUXDB_PORT}",
    token=Config.INFLUXDB_TOKEN
)
write_api = client.write_api()

def save_to_influxdb(request_type, name, response_time, response_length, exception):
    try:
        data = f'locust_test,request_type={request_type},name={name} response_time={response_time},response_length={response_length} {int(time.time() * 1e9)}'
        write_api.write(Config.INFLUXDB_BUCKET, Config.INFLUXDB_ORG, data)
        logging.info(f"✅ Logged request: {request_type}, {name}, {response_time} ms")
        # Flush the log immediately
        logging.getLogger().handlers[0].flush()
    except Exception as e:
        logging.error(f"❌ Failed to write to InfluxDB: {e}")
        logging.getLogger().handlers[0].flush()

# Event listener to log and save results
@events.request.add_listener
def request_listener(request_type, name, response_time, response_length, exception, **kwargs):
    logging.info(f"📌 Request logged: {request_type}, {name}, {response_time} ms")
    logging.getLogger().handlers[0].flush()
    save_to_influxdb(request_type, name, response_time, response_length, exception)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)

# Close InfluxDB client after test
@events.test_stop.add_listener
def on_test_stop(**kwargs):
    client.close()
    logging.info("✅ InfluxDB client closed.")
    logging.getLogger().handlers[0].flush()
