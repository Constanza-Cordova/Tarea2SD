import csv
import grpc
import pedido_pb2
import pedido_pb2_grpc

def realizar_pedidos_desde_csv(archivo_csv):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pedido_pb2_grpc.PedidoServiceStub(channel)
        with open(archivo_csv, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                response = stub.RealizarPedido(pedido_pb2.PedidoRequest(
                    id=row['id'],
                    descripcion=row['descripcion'],
                    nombre_producto=row['nombre_producto'],
                    precio=float(row['precio']),
                    pasarela_pago=row['pasarela_pago'],
                    marca_tarjeta=row['marca_tarjeta'],
                    banco=row['banco'],
                    region_envio=row['region_envio'],
                    direccion_envio=row['direccion_envio'],
                    correo_cliente=row['correo_cliente']
                ))
                print(f"Pedido {row['id']} status: {response.status}")

if __name__ == '__main__':
    realizar_pedidos_desde_csv('orders.csv')
