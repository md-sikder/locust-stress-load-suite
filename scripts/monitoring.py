import logging
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from config.config import Config

# Ensure 'logs' directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging (Saves logs to a file + prints to console)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/performance_test.log"),  # Save to file
        logging.StreamHandler()  # Print to console
    ]
)

# Initialize InfluxDB client
client = InfluxDBClient(
    url=f"http://{Config.INFLUXDB_HOST}:{Config.INFLUXDB_PORT}",
    token=Config.INFLUXDB_TOKEN,
    org=Config.INFLUXDB_ORG
)
write_api = client.write_api()

def save_to_influxdb(request_type, name, response_time, response_length, exception):
    try:
        point = Point("performance_test") \
            .field("request_type", request_type) \
            .field("name", name) \
            .field("response_time", response_time) \
            .field("response_length", response_length) \
            .field("exception", str(exception) if exception else "None") \
            .time(datetime.utcnow())

        write_api.write(bucket=Config.INFLUXDB_BUCKET, record=point)
        logging.info(f"✅ Data written to InfluxDB: {request_type}, {name}, {response_time} ms")
        logging.getLogger().handlers[0].flush()
    except Exception as e:
        logging.error(f"❌ InfluxDB Write Error: {e}")
        logging.getLogger().handlers[0].flush()

