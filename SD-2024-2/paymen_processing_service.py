from confluent_kafka import Consumer, KafkaError

def process_payment():
    consumer_conf = {
        'bootstrap.servers': 'localhost:9093',
        'group.id': 'payment-processor',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['pedidos'])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            pedido = msg.value().decode('utf-8').split(',')
            print(f"Procesando pago para el pedido {pedido[0]}")

            # Aquí se puede añadir la lógica para procesar el pago
            # Por ejemplo, integrarse con una pasarela de pago

    except KeyboardInterrupt:
        print("Procesamiento interrumpido manualmente.")
    finally:
        consumer.close()
        print("Consumer cerrado correctamente.")

if __name__ == "__main__":
    process_payment()
