"""This script is not executable as a python script;
Instead, it should be executed line-by-line in pyspark shell, opened with:
  ```
  pyspark --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11
  ```
"""

from graphframes import *
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

# Load pre-computed similarity data and construct graph.
import _pickle as pkl
doc_sim = pkl.load(open('doc_sim.pkl', 'rb'))
v = sqlContext.createDataFrame(doc_sim['vertices'], ['id'])
e = sqlContext.createDataFrame(doc_sim['edges'], ['src', 'dst', 'relationship'])
g = GraphFrame(v, e)

# PageRank
results = g.pageRank(resetProbability=0.15, maxIter=10)
results.vertices.select('id', 'pagerank').show()
results.edges.select('src', 'dst', 'weight').show()

# Triangle Count
results = g.triangleCount()
results.select("id", "count").show()

# Connected Components
from pyspark.sql.functions import desc
sc.setCheckpointDir('./')
results = g.connectedComponents()
results.select("id", "component").orderBy(desc("component")).show()