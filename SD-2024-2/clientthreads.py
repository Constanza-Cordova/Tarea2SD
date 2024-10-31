import csv
import asyncio
import grpc
import pedido_pb2
import pedido_pb2_grpc
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

async def realizar_pedido_async(
    stub: pedido_pb2_grpc.PedidoServiceStub,
    pedido: Dict[str, str]
) -> None:
    try:
        response = await stub.RealizarPedido(
            pedido_pb2.PedidoRequest(
                id=pedido['id'],
                descripcion=pedido['descripcion'],
                nombre_producto=pedido['nombre_producto'],
                precio=float(pedido['precio']),
                pasarela_pago=pedido['pasarela_pago'],
                marca_tarjeta=pedido['marca_tarjeta'],
                banco=pedido['banco'],
                region_envio=pedido['region_envio'],
                direccion_envio=pedido['direccion_envio'],
                correo_cliente=pedido['correo_cliente']
            )
        )
        print(f"Pedido {pedido['id']} status: {response.status}")
    except Exception as e:
        print(f"Error en pedido {pedido['id']}: {str(e)}")

async def procesar_pedidos_batch(
    pedidos: List[Dict[str, str]], 
    batch_size: int = 50
) -> None:
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = pedido_pb2_grpc.PedidoServiceStub(channel)
        
        for i in range(0, len(pedidos), batch_size):
            batch = pedidos[i:i + batch_size]
            tareas = [realizar_pedido_async(stub, pedido) for pedido in batch]
            await asyncio.gather(*tareas)

def leer_pedidos_csv(archivo_csv: str) -> List[Dict[str, str]]:
    pedidos = []
    with open(archivo_csv, mode='r') as file:
        csv_reader = csv.DictReader(file)
        pedidos.extend(list(csv_reader))
    return pedidos

async def main():
    # Leer todos los pedidos del CSV
    pedidos = leer_pedidos_csv('pedidos.csv')
    
    # Procesar los pedidos en batches
    await procesar_pedidos_batch(pedidos)

if __name__ == '__main__':
    asyncio.run(main())
