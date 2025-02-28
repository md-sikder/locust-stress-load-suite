# import os
#
# # Configuration values (can be read from environment variables or config files)
# class Config:
#     THRESHOLD_RESPONSE_TIME = int(os.getenv('THRESHOLD_RESPONSE_TIME', 2000))  # ms
#     THRESHOLD_ERROR_RATE = float(os.getenv('THRESHOLD_ERROR_RATE', 5))  # %
#     INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', 'localhost')
#     INFLUXDB_PORT = int(os.getenv('INFLUXDB_PORT', 8086))
#     INFLUXDB_DBNAME = os.getenv('INFLUXDB_DBNAME', 'performance_metrics')
#     INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '')  # <-- Add this line
#     LOCUST_USERS = int(os.getenv('LOCUST_USERS', 100))
#     LOCUST_HATCH_RATE = int(os.getenv('LOCUST_HATCH_RATE', 10))
#     LOCUST_TEST_DURATION = os.getenv('LOCUST_TEST_DURATION', '5m')
#
import os


class Config:
    THRESHOLD_RESPONSE_TIME = int(os.getenv('THRESHOLD_RESPONSE_TIME', 2000))  # ms
    THRESHOLD_ERROR_RATE = float(os.getenv('THRESHOLD_ERROR_RATE', 5))  # %

    # InfluxDB Configuration
    INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', 'localhost')
    INFLUXDB_PORT = int(os.getenv('INFLUXDB_PORT', 8086))
    INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET', 'performance_metrics')  # Fixed
    INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'my-org')  # Add Organization
    INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN', '')

    # Locust Load Testing Parameters
    LOCUST_USERS = int(os.getenv('LOCUST_USERS', 100))
    LOCUST_HATCH_RATE = int(os.getenv('LOCUST_HATCH_RATE', 10))
    LOCUST_TEST_DURATION = os.getenv('LOCUST_TEST_DURATION', '5m')
