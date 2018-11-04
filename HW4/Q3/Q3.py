'''This script is not executable as a python script;
Instead, it should be executed line-by-line in pyspark shell, opened with:
  ```
  pyspark --packages graphframes:graphframes:0.6.0-spark2.3-s_2.11
  ```
'''

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
pr_results = g.pageRank(resetProbability=0.15, maxIter=10)
# Connected Components
sc.setCheckpointDir('./')
cc_results = g.connectedComponents()

pr_v = pr_results.vertices.select('id', 'pagerank').collect()
pr_e = pr_results.edges.select('src', 'dst', 'weight').collect()
cc = cc_results.select('id', 'component').collect()

node_pr = {v.id: v.pagerank for v in pr_v}
node_cc = {v.id: v.component for v in cc}

fnode = open('node.csv', 'w')
fnode.write('{},{},{}\n'.format('ID', 'PageRank', 'Component'))
for k, v in node_pr.items():
  if k in node_cc:
    fnode.write('{},{},{}\n'.format(k, v, node_cc[k]))

fedge = open('edge.csv', 'w')
fedge.write('{},{}\n'.format('source', 'target'))
for e in pr_e:
  fedge.write('{},{}\n'.format(e.src, e.dst))
