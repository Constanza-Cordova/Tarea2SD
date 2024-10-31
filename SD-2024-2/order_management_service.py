import grpc
from concurrent import futures
import pedido_pb2
import pedido_pb2_grpc
from confluent_kafka import Producer

class PedidoService(pedido_pb2_grpc.PedidoServiceServicer):
    def RealizarPedido(self, request, context):
        print(f"Procesando pedido de {request.nombre_producto} para {request.correo_cliente}")
        mensaje = f"{request.id},{request.descripcion},{request.nombre_producto},{request.precio},{request.pasarela_pago},{request.marca_tarjeta},{request.banco},{request.region_envio},{request.direccion_envio},{request.correo_cliente}"
        enviar_a_kafka(mensaje)
        return pedido_pb2.PedidoResponse(status="Procesando")

def enviar_a_kafka(mensaje):
    producer = Producer({'bootstrap.servers': 'localhost:9093'})
    producer.produce('pedidos', mensaje.encode('utf-8'))
    producer.flush()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pedido_pb2_grpc.add_PedidoServiceServicer_to_server(PedidoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
