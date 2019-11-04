from pyspark.ml.linalg import VectorUDT
from pyspark.sql.functions import *
from pyspark.ml.linalg import DenseVector
from pyspark.ml.clustering import KMeans

vectors = spark.read.csv("version2_pca50")
vectors = vectors.selectExpr("_c0 as Label", "_c1 as PCA")

one = udf(lambda row: DenseVector([float(number) for number in row.split(",")]), VectorUDT())
vecKM = vectors.withColumn("features", one(vectors['PCA']))

features = vecKM.select("features")
results = []
errors = {}
for k in range(10, 1000, 10): #best k = 150
    kmeans = KMeans().setK(k).setSeed(1)
    model = kmeans.fit(features)
    wssse = model.computeCost(vecKM)
    results.append([k, wssse])
    print("k " + str(k) + ": Error " + str(wssse))
    errors[str(k)] = str(wssse)
    predictions = model.transform(features)
    predictions.show()


for k, v in errors.items():
    print(k, v)
