import warnings
import logging
import os
from dotenv import load_dotenv, find_dotenv
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()
logger.info("creating spark session")
conf = SparkConf()\
        .setAll([
            ("spark.driver.extraClassPath", "/Users/olorunleke.akindote/google-cloud-bigquery-2.31.0.jar"),
            ("spark.jars.packages", "mysql:mysql-connector-java:8.0.15"),
            ("spark.executor.extraClassPath", "/Users/olorunleke.akindote/google-cloud-bigquery-2.31.0.jar"),
            ("google.cloud.auth.service.account.enable", "true"),
            ("google.cloud.auth.service.account.json.keyfile", "/path/to/keyfile.json"),
            ("spark.sql.execution.arrow.enabled", "true")
        ])

sc = SparkContext(conf=conf)
spark = SparkSession(sc).builder \
    .appName("database-read-write") \
    .getOrCreate()
# load all environment variables 
load_dotenv(find_dotenv())

# specifying BigQuery connection parameters
project_id = "<project_id>"
dataset_name = "<dataset_name>"
table_name = "<table_name>"

# specifying database connection parameters
url = "jdbc:mysql://localhost:3306/employees?serverTimezone=UTC"
properties = {
    "user": os.environ.get("USERNAME"),
    "password": os.environ.get("PASSWORD"),
    "driver": "com.mysql.cj.jdbc.Driver"
}
table_name = "employees_transformed"

# Read data from MYSQL database
df = spark.read.jdbc(url=url, table=table_name, properties=properties)

#show dataframe
# df.show()

# write dataframe to BigQuery
df.write \
    .format("bigquery") \
    .option("table", f"{project_id}:{dataset_name}.{table_name}") \
    .mode("overwrite") \
    .save()


