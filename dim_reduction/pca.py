# pyspark --master yarn --executor-cores 2 --driver-cores 10 --num-executors 15 --executor-memory 10G --driver-memory 30G

from pyspark.ml.linalg import VectorUDT
from pyspark.sql.functions import *
from pyspark.ml.linalg import DenseVector
from pyspark.ml.feature import PCA

vectorsF = sc.textFile("sparkvectors2019") 
vectorsR = vectorsF.map(lambda row: (row.split(" - ")[0], row.split(" - ")[1]))

vectorsDF = spark.createDataFrame(vectorsR, ['Label', 'Vector'])

vectorsDF.count()

one = udf(lambda row: DenseVector([float(number) for number in row.split(",")]), VectorUDT())
vecPCA = vectorsDF.withColumn("DenseVector", one(vectorsDF['Vector']))


for k in range(2, 20, 2):
    pca = PCA(k=k, inputCol="DenseVector", outputCol="pcaFeatures")
    model = pca.fit(vecPCA)
    model.explainedVariance
    result = model.transform(vecPCA)
    result.rdd.map(lambda row: row[0] + ",\"" + ",".join(str(a) for a in row[3]) + "\"").saveAsTextFile("version2_pca" + str(k))



