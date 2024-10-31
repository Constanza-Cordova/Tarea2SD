import csv
import grpc
import pedido_pb2
import pedido_pb2_grpc
import time
import random

def realizar_pedidos_desde_csv(archivo_csv):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pedido_pb2_grpc.PedidoServiceStub(channel)
        with open(archivo_csv, mode='r') as file:
            csv_reader = csv.DictReader(file)
            start_time = time.time()

            for row in csv_reader:
                # Crear la solicitud para el pedido
                request = pedido_pb2.PedidoRequest(
                    id=int(row['id']),
                    descripcion=row['descripcion'],
                    nombre_producto=row['nombre_producto'],
                    precio=float(row['precio']),
                    pasarela_pago=row['pasarela_pago'],
                    marca_tarjeta=row['marca_tarjeta'],
                    banco=row['banco'],
                    region_envio=row['region_envio'],
                    direccion_envio=row['direccion_envio'],
                    correo_cliente=row['correo_cliente']
                )

                # Enviar la solicitud y recibir la respuesta
                response = stub.RealizarPedido(request)
                print(f"Pedido {row['id']} status: {response.status}")

                # Retraso aleatorio entre 100 ms y 1 segundo
                time.sleep(random.uniform(0.1, 1.0))

            elapsed_time = time.time() - start_time
            print(f"Finalizó el envío de pedidos en {elapsed_time:.2f} segundos.")

if __name__ == '__main__':
    realizar_pedidos_desde_csv('orders.csv')  # Asegúrate de que el archivo CSV esté en el mismo directorio
