from pyspark.sql.types import StructType, StructField, FloatType, LongType, IntegerType, StringType
from pyspark.sql.functions import *

rfrdd = spark.read.format("csv").option("header", "false").load("pca150kmeans150")

joined = rfrdd.selectExpr('_c0 as Cluster', '_c1 as Label', '_c3 as Coordinates')

label_freq = joined.groupBy('Label').count()
joined_freq = joined.join(label_freq, 'Label')
cluster_freq = joined.groupBy(['Label', 'Cluster']).count()
cluster_freq = cluster_freq.selectExpr("Label as Label", "Cluster as Cluster", "count as WordClusterCount")


result = joined_freq.join(cluster_freq, (cluster_freq.Label == joined_freq.Label) & (cluster_freq.Cluster == joined_freq.Cluster))

from math import floor

def threshold(row):
    return row * 0.1

thresholding = udf(lambda row: floor(threshold(row * 0.1)), FloatType())
result2 = result.withColumn('threshold', thresholding('count'))
result2.createOrReplaceTempView('result2')
total_result = spark.sql("SELECT * FROM result2 WHERE WordClusterCount > threshold")
total_rdd = total_result.rdd
reduced_rdd = total_rdd.map(lambda row: row[2:])

mySchema = StructType([StructField("Coordinates", StringType(), True), StructField("count", IntegerType(), True), StructField("Label", StringType(), True), StructField("Cluster", StringType(),True), StructField('WordCountCluster', IntegerType(), True), StructField("threshold", FloatType(),True)])

reduced_df = spark.createDataFrame(reduced_rdd, mySchema)
final_result = reduced_df.groupby(['Label', 'Cluster', 'Coordinates']).count()
resultRDD = final_result.rdd.map(lambda row: ((row[0], row[1]), "(" + row[2] + ")")).reduceByKey(lambda x, y: x + "," + y).map(lambda row: (row[0][0], row[0][1], row[1]))
mmschema = StructType([StructField("Label", StringType(), True), StructField("Cluster", StringType(), True), StructField("Coordinates", StringType(), True)])
resultDF = spark.createDataFrame(resultRDD, mmschema)

#resultDF.show()


from ast import literal_eval as make_tuple
def mean_vector(vectors):
    vectors = vectors.replace("(", "").replace(")","")
    vectors = [[vectors.split(",")[i], vectors.split(",")[i+1]] for i in range(0, len(vectors.split(",")), 2)]
    total = len(vectors)
    avg = [0, 0]
    for v in vectors:
        avg[0] += float(v[0])
        avg[1] += float(v[1])
        avg = [str(avg[0]/float(total)), str(avg[1]/float(total))]
        return "(" + ", ".join(avg) + ")"

meve = udf(lambda row: mean_vector(row), StringType())
redf = resultDF.withColumn('Mean', meve("Coordinates"))
redf.show()
redf.write.csv("random_name")
