from confluent_kafka import Consumer, Producer, KafkaError
from elasticsearch import Elasticsearch
import time

es = Elasticsearch(["http://localhost:9200"])

# Variables para métricas
request_count = 0
start_time = time.time()  # Inicializa start_time al inicio del programa

# Función para almacenar las métricas de latencia
def store_latency_metrics(elapsed_time):
    metrics = {
        "service": "sts_service",
        "latency_notificaciones": elapsed_time,
        "timestamp": time.time()
    }
    es.index(index="metrics", document=metrics)  # Almacena la métrica en el índice "metrics"
    print(f"Métrica de latencia guardada: {elapsed_time} segundos")

# Función para almacenar las métricas de throughput
def store_throughput_metrics():
    global request_count  # Solo request_count necesita ser global
    global start_time  # Declarar start_time como global aquí

    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        throughput = request_count / elapsed_time  # mensajes por segundo
        throughput_metrics = {
            "service": "sts_service",
            "throughput_notificaciones": throughput,
            "timestamp": time.time()
        }
        es.index(index="metrics_sts", document=throughput_metrics)
        print(f"Métrica de throughput guardada: {throughput} mensajes por segundo")
    
    # Reiniciar contadores
    request_count = 0
    start_time = time.time()  # Reinicia start_time al final de la función

def consumir_y_producir(topico_origen, topico_destino):
    consumer_conf = {
        'bootstrap.servers': 'localhost:9093',
        'group.id': 'grupo-consumidor-productor',
        'auto.offset.reset': 'earliest'
    }
    producer_conf = {
        'bootstrap.servers': 'localhost:9093'
    }

    consumer = Consumer(consumer_conf)
    producer = Producer(producer_conf)
    consumer.subscribe([topico_origen])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            mensaje = msg.value().decode('utf-8')
            print(f"Mensaje recibido en {topico_origen}: {mensaje}")

            # Marca el inicio del procesamiento para latencia
            start_processing_time = time.time()

            # Producir el mensaje en el siguiente tópico
            producer.produce(topico_destino, mensaje.encode('utf-8'))
            producer.flush()

            # Calcular el tiempo de procesamiento
            elapsed_time = time.time() - start_processing_time
            store_latency_metrics(elapsed_time)  # Almacena la métrica de latencia

            # Confirmar el commit del offset
            consumer.commit(msg)
            print(f"Mensaje producido en {topico_destino}: {mensaje}")

            # Incrementar el contador de pedidos procesados
            global request_count
            request_count += 1

            # Enviar métricas de throughput cada 10 mensajes
            if request_count % 10 == 0:  # Puedes ajustar este número según la necesidad
                store_throughput_metrics()

    except KeyboardInterrupt:
        print("Consumo y producción interrumpida manualmente.")
    finally:
        consumer.close()
        print("Consumer cerrado correctamente.")

if __name__ == "__main__":
    # Ejemplo de transición de estados
    consumir_y_producir('procesando', 'preparacion')
    consumir_y_producir('preparacion', 'enviado')
    consumir_y_producir('enviado', 'entregado')
    consumir_y_producir('entregado', 'finalizado')
