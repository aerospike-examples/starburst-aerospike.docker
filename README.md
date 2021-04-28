# starburst-aerospike-docker
[Starburst Enterprise Trino](https://docs.starburst.io/starburst-enterprise/) with the [Aeropsike connector](https://www.aerospike.com/enterprise/download/connectors/aerospike-trino) Docker Image.

## Quickstart
Build a Docker image.
Make sure to adjust the server and the connector configuration in the `docker/etc` folder.
You can pass the `STARBURST_VERSION` and the `CONNECTOR_VERSION` [arguments](https://docs.docker.com/engine/reference/builder/#arg) with the docker build command.
```bash
docker build . -t starburst-aerospike
```

To launch it, execute the following:
```bash
docker run --rm -p 8080:8080 --name starburst-aerospike starburst-aerospike
```
Below is the list of environment variables you can specify to configure the Trino server and the Aerospike connector using the [-e](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) option.

| Variable | Description | Default Value |
| --- | --- | --- |
| AS_HOSTLIST | Aerospike host list, a comma separated list of potential hosts to seed the cluster. |  |
| TABLE_DESC_DIR | Path of the directory containing table description files.<sup>[1](#schema-folder)</sup> | /etc/starburst/aerospike |
| SPLIT_NUMBER | Number of Trino splits. See Parallelism section for more information. | 4 |
| CACHE_TTL_MS | Number of milliseconds to keep the inferred schema cached. | 1800000 |
| STRICT_SCHEMAS | Use a strict schema.<sup>[2](#strict-schema)</sup> | false |
| DEFAULT_SET_NAME | Table name for the default set. This is used when your namespace has a null set or no sets. | __default |
| RECORD_KEY_NAME | Column name for the record's primary key. Use this in the WHERE clause for queries involving primary key (PK) comparisons. | __key |
| RECORD_KEY_HIDDEN | If set to false, the primary key column will be available in the result set. | true |
| INSERT_REQUIRE_KEY | Require the primary key on INSERT queries. Although we recommend that you provide a primary key, you can choose not to by setting this property to false, in which case a UUID is generated for the PK. You can view it by setting aerospike.record-key-hidden to false for future queries. | true |
| TRINO_DISCOVERY_URI | The URI to the Discovery server. This should be the URI of the Trino coordinator. Replace the default value to match the host and port of the Trino coordinator. This URI must not end in a slash. | http://localhost:8080 |
| TRINO_NODE_TYPE | The Trino node type, can be either `coordinator` or `worker`. | `single-node` |

<sup name="schema-folder">1</sup> To set the required schema configuration, bind-mount the table description folder on `docker run`.
```
-v "$(pwd)"/docker/etc/aerospike:/etc/starburst/aerospike
```

Wait for the following message log line:
```
INFO	main	io.trino.server.Server	======== SERVER STARTED ========
```

The Trino server is now running on `localhost:8080` (the default port).

## Multi-Node Starburst Enterprise Trino Cluster
To run a Trino cluster of one coordinator and one worker:
* Start a Trino coordinator.
```
docker run --rm -p 8080:8080 -e TRINO_NODE_TYPE=coordinator -e AS_HOSTLIST=docker.for.mac.host.internal:3000 --name trino-aerospike-coordinator starburst-aerospike
```
* Start a Trino worker<sup>[1](#worker)</sup>, specify the `TRINO_DISCOVERY_URI` to be the URI of the Trino coordinator.
```
docker run --rm -e TRINO_NODE_TYPE=worker -e AS_HOSTLIST=docker.for.mac.host.internal:3000 -e TRINO_DISCOVERY_URI=http://172.17.0.3:8080 --name trino-aerospike-worker starburst-aerospike
```
<sup name="worker">1</sup> Run this command number of times with different container names to add more workers.
