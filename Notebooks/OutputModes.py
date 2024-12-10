from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

if __name__ == '__main__':
    spark = SparkSession.builder.appName("Spark Streaming Demo").master("local").getOrCreate()

    CRIME_DATA_SCHEMA = StructType([
        StructField("incident_id", StringType()),
        StructField("location", StringType()),
        StructField("crime_type", StringType())
    ]
    )

    # Source
    inputDF = spark.readStream.load(path="../../resources/dataset/crime_data/input",
                                    format="csv",
                                    schema=CRIME_DATA_SCHEMA)


    # Incremental Query
    # resultDf = inputDF.filter(col("location")=="Downtown")
    resultDF = inputDF.groupBy("location").agg(count("*").alias("total_count"))

    # Output Sink
    resultDF.writeStream.start(format="console", outputMode="update").awaitTermination()

