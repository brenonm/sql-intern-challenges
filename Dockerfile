FROM postgres:16

COPY initdb/ /docker-entrypoint-initdb.d/
COPY data/ /data/