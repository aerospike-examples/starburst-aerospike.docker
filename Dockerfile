#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
ARG STARBURST_VERSION=371-e

FROM starburstdata/starburst-enterprise:${STARBURST_VERSION}

ARG CONNECTOR_VERSION=3.1.0

USER root:root
RUN \
    microdnf -y install unzip ca-certificates wget libuuid gettext && \
    wget -q -O /tmp/aerospike.zip "https://www.aerospike.com/artifacts/enterprise/aerospike-trino/$CONNECTOR_VERSION/aerospike-trino-$CONNECTOR_VERSION.zip" && \
    unzip -q /tmp/aerospike.zip -d /tmp && \
    mv /tmp/trino-aerospike-$CONNECTOR_VERSION /usr/lib/starburst/plugin/aerospike && \
    chown -R starburst:root /usr/lib/starburst/plugin/aerospike

COPY --chown=starburst:root docker/etc/catalog /etc/starburst/catalog
COPY template setup.sh /tmp/

RUN chmod 0777 /tmp/setup.sh

CMD ["/tmp/setup.sh"]
