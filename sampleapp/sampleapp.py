# IP Address or DNS name for one host in your Aerospike cluster
AS_HOST = "127.0.0.1"

AS_PORT = 3000 # Usually 3000, but change here if not

import aerospike
import csv

# Configure the client
config = {
  'hosts': [ (AS_HOST, AS_PORT) ]
}

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)


def null_int(str):
    try:
        return int(str)
    except ValueError as e:
        return 0

pk = []
namespace = "test"
write_set = "natality_demo"

count = 0
with open('natality.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    next(readCSV, None)    
    for  row in readCSV:
      _c1,_c2,_c3,_c4,_c5,_c6 = row
      c1 = float(_c1)
      c2 = null_int(_c2)
      c3 = null_int(_c3)
      c4 = null_int(_c4)
      c5 = null_int(_c5)
      c6 = null_int(_c6)
      count = count + 1
      pk.append(count)  
      #print (c1,c2,c3,c4,c5,c6,count)

      key = (namespace, write_set, count)
      client.put(key, {'weight_pnd': c1,
                 'mother_age': c2,
                 'father_age': c3,
                 'gstation_week': c4,
                 'weight_gain_pnd': c5,
                 'apgar_5min': c6,
                 })


for  x in pk:
    key = (namespace, write_set,x)
    (key, metadata, record) = client.get(key)
    #print(record)