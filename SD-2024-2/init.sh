#!/bin/bash

# Variables de entorno para configuraciones
PARTITIONS=${PARTITIONS:-3}  # Número de particiones por defecto (puedes cambiarlo)
REPLICATION_FACTOR=${REPLICATION_FACTOR:-2}  # Factor de replicación por defecto
BALANCING_POLICY=${BALANCING_POLICY:-"rack"}  # Ejemplo de política de balanceo de carga

# Crear los tópicos usando el nombre especificado en la variable de entorno TOPIC_NAMES
IFS=',' read -r -a topics <<< "$TOPIC_NAMES"

for topic in "${topics[@]}"; do
    /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topic" \
        --bootstrap-server kafka1:9092 \
        --partitions "$PARTITIONS" \
        --replication-factor "$REPLICATION_FACTOR" \
        --config "replication.factor=$REPLICATION_FACTOR" \
        --config "min.insync.replicas=1"  # Ejemplo de política de balanceo de carga

    echo "Topic $topic created with $PARTITIONS partitions and replication factor of $REPLICATION_FACTOR"
done
