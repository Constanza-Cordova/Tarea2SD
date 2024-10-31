from confluent_kafka import Consumer

def consume():
    # Configuración del Consumer
    consumer_conf = {
        'bootstrap.servers': 'localhost:9093', #9093
        'group.id': 'grupo-consumidor1',
        'auto.offset.reset': 'earliest'  # Empieza desde el principio si no hay un offset guardado
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['pedidos'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)  # Espera 1 segundo por mensajes
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            print(f"Mensaje recibido: key={msg.key().decode('utf-8') if msg.key() else 'N/A'}, "
                  f"value={msg.value().decode('utf-8')}, partition={msg.partition()}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume()
