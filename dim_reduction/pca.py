# PySpark parameters used
# --executor-cores 2 --driver-cores 10 -num-executors 15 --executor-memory 10G --driver-memory 30G
from pyspark.ml.linalg import DenseVector, VectorUDT
from pyspark.ml.feature import PCA
from pyspark.sql.functions import *

# Each line of the Input file follows this format:
# "word - 0.6579854,1.161026,0.43898278,[...],2.0629232,0.063231304"
input_file = "sparkvectors2019"

# Maximum PCA dimension
K = 20

# Read the file, parse it as RDD and transform it into DataFrame
raw_vectors = sc.textFile(input_file)
vectors_rdd = raw_vectors.map(lambda row:
                              (row.split(" - ")[0], row.split(" - ")[1]))
vectors_df = spark.createDataFrame(vectors_rdd, ['Label', 'Vector'])

# Count the elements to force Spark to load the file at this time
vectors_df.count()

# Parse vectors as DenseVectors
vectorize_lines = udf(lambda row:
                      DenseVector([float(number) for number in row.split(",")]), VectorUDT())
vectorized_df = vectors_df.withColumn(
    "DenseVector", vectorize_lines(vectors_df['Vector']))

pca = PCA(k=K, inputCol="DenseVector", outputCol='pcaFeatures')
model = pca.fit(vectorized_df)
# model.explainedVariance
result = mode.transform(vectorized_df)
for k, in range(1, K):
    result.rdd.map(lambda row:
                   row[0] + ",\"" + ",".join(str(a) for a in row[3][:k]) + "\"").saveAsTextFile("pca" + str(k))
