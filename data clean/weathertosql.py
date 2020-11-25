from __future__ import print_function
from pyspark.sql import SparkSession
import pyspark.sql.functions as fc


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("q1") \
        .getOrCreate()
    csv_file_path = 'weather_description.csv'
    weather = spark.read.options(header='True',inferSchema='True',delimiter=',')\
        .csv(csv_file_path)
    df = weather.select(fc.split("datetime"," ").getItem(0).alias("date"),fc.split("datetime"," ")\
        .getItem(1).alias("hour"),fc.col("Los Angeles").alias("weather")).drop("datetime")
    df2 = df.select("weather",fc.date_format(fc.unix_timestamp('hour',"H:mm").cast("timestamp"),"HH").alias('hour'),\
        fc.to_date(fc.unix_timestamp('date',"M/d/yyyy").cast("timestamp"),"yyyy-MM-dd").alias('date'))\
        .where("weather is not null")
    df2.coalesce(1).write.csv('weatherToSQL',header='true')
    spark.stop()
