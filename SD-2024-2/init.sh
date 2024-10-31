#!/bin/bash

# Crear los tópicos usando el nombre especificado en la variable de entorno TOPIC_NAMES
IFS=',' read -r -a topics <<< "$TOPIC_NAMES"

for topic in "${topics[@]}"; do
    /opt/bitnami/kafka/bin/kafka-topics.sh --create --topic "$topic" --bootstrap-server kafka1:9092 --partitions 1 --replication-factor 1
    echo "Topic $topic created"
done
