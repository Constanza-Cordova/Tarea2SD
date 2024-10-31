import grpc
from concurrent import futures
import pedido_pb2
import pedido_pb2_grpc
from confluent_kafka import Producer
from elasticsearch import Elasticsearch
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time  # Importamos time para medir la latencia
from threading import Timer  # Para manejar el envío de métricas periódicas

class PedidoService(pedido_pb2_grpc.PedidoServiceServicer):
    def __init__(self):
        self.request_count = 0  # Contador de pedidos procesados
        self.start_time = time.time()  # Marca el inicio del tiempo
        self.es = Elasticsearch(["http://localhost:9200"])  # Conexión a Elasticsearch
        self.start_metrics_timer()  # Inicia el temporizador para enviar métricas

    def RealizarPedido(self, request, context):
        start_time = time.time()  # Marca el inicio del procesamiento
        try:
            print(f"Procesando pedido de {request.nombre_producto} para {request.correo_cliente}")
            mensaje = f"{request.id},{request.descripcion},{request.nombre_producto},{request.precio},{request.pasarela_pago},{request.marca_tarjeta},{request.banco},{request.region_envio},{request.direccion_envio},{request.correo_cliente}"
            enviar_a_kafka(mensaje)
            enviar_a_elasticsearch(request)  # Nueva función para Elasticsearch
            enviar_correo(request.correo_cliente, request.nombre_producto)

            # Calcular latencia
            latency = time.time() - start_time
            self.store_metrics(latency)  # Almacena métricas de latencia

            # Incrementar el contador de pedidos procesados
            self.request_count += 1  

            # Enviar métricas de notificaciones
            self.store_notification_metrics(request.id, latency)

            return pedido_pb2.PedidoResponse(status="Procesando")
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return pedido_pb2.PedidoResponse(status="Error")

    def store_metrics(self, latency):
        # Guardar las métricas de latencia en Elasticsearch
        metrics = {
            "service": "pedido_service",
            "latency": latency,
            "timestamp": time.time()
        }
        self.es.index(index="metrics", document=metrics)  # Almacena la métrica en el índice "metrics"
        print(f"Métrica de latencia guardada: {latency} segundos")

    def store_notification_metrics(self, pedido_id, latency):
        # Guardar métricas de latencia y throughput de notificaciones
        notification_metrics = {
            "pedido_id": pedido_id,
            "latencia_notificaciones": latency,
            "timestamp": time.time()
        }
        self.es.index(index="metricas-notificaciones", document=notification_metrics)

    def start_metrics_timer(self):
        # Inicia un temporizador para enviar métricas de throughput cada 10 segundos
        Timer(10, self.send_throughput).start()

    def send_throughput(self):
        # Calcular throughput
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            throughput = self.request_count / elapsed_time  # pedidos por segundo
            # Almacenar throughput en Elasticsearch
            throughput_metrics = {
                "service": "pedido_service",
                "throughput": throughput,
                "timestamp": time.time()
            }
            self.es.index(index="metrics", document=throughput_metrics)
            print(f"Métrica de throughput guardada: {throughput} pedidos por segundo")

        # Reiniciar contadores
        self.request_count = 0
        self.start_time = time.time()

        # Reiniciar el temporizador
        self.start_metrics_timer()

def enviar_a_kafka(mensaje):
    producer = Producer({'bootstrap.servers': 'localhost:9093'})
    producer.produce('procesando', mensaje.encode('utf-8'))
    producer.flush()

def enviar_a_elasticsearch(request):
    es = Elasticsearch(["http://localhost:9200"])  # Conexión a Elasticsearch en el puerto predeterminado
    doc = {
        "id": request.id,
        "descripcion": request.descripcion,
        "nombre_producto": request.nombre_producto,
        "precio": request.precio,
        "pasarela_pago": request.pasarela_pago,
        "marca_tarjeta": request.marca_tarjeta,
        "banco": request.banco,
        "region_envio": request.region_envio,
        "direccion_envio": request.direccion_envio,
        "correo_cliente": request.correo_cliente
    }
    response = es.index(index="pedidos", document=doc)
    print(f"Pedido registrado en Elasticsearch con ID: {response['_id']}")

def enviar_correo(correo_cliente, nombre_producto):
    remitente = "saidai003s@gmail.com"
    destinatario = correo_cliente
    asunto = "Confirmación de Pedido"
    cuerpo = f"Tu pedido de {nombre_producto} ha sido recibido y está siendo procesado."

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        servidor_smtp = smtplib.SMTP("smtp.gmail.com", 587)
        servidor_smtp.starttls()
        servidor_smtp.login(remitente, "iutz vwyl ushk gtjg")  # Aquí va la contraseña
        servidor_smtp.sendmail(remitente, destinatario, mensaje.as_string())
        servidor_smtp.quit()
        print(f"Correo enviado a {correo_cliente}")
    except Exception as e:
        print(f"Error al enviar correo: {e}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pedido_pb2_grpc.add_PedidoServiceServicer_to_server(PedidoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
