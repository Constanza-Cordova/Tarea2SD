from confluent_kafka import Consumer, KafkaError
import smtplib
from email.mime.text import MIMEText

def send_notification():
    consumer_conf = {
        'bootstrap.servers': 'localhost:9093',
        'group.id': 'notification-service',
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
            correo_cliente = pedido[9]
            mensaje = f"Tu pedido {pedido[0]} está en estado: Procesando"

            print(f"Enviando notificación a {correo_cliente}")
            enviar_correo(correo_cliente, "Actualización de Pedido", mensaje)

    except KeyboardInterrupt:
        print("Notificación interrumpida manualmente.")
    finally:
        consumer.close()
        print("Consumer cerrado correctamente.")

def enviar_correo(destinatario, asunto, cuerpo):
    remitente = "tuemail@example.com"
    mensaje = MIMEText(cuerpo)
    mensaje['Subject'] = asunto
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    try:
        with smtplib.SMTP('smtp.example.com') as server:
            server.login(remitente, "tu_password")
            server.sendmail(remitente, [destinatario], mensaje.as_string())
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

if __name__ == "__main__":
    send_notification()
