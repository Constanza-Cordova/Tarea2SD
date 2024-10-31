class Pedido:
    estados = ["Procesando", "Preparación", "Enviado", "Entregado", "Finalizado"]

    def __init__(self):
        self.estado_actual = self.estados[0]

    def siguiente_estado(self):
        indice_actual = self.estados.index(self.estado_actual)
        if indice_actual < len(self.estados) - 1:
            self.estado_actual = self.estados[indice_actual + 1]
        else:
            print("El pedido ya está en el estado final.")

    def __str__(self):
        return f"Estado actual del pedido: {self.estado_actual}"

# Ejemplo de uso:
pedido = Pedido()
print(pedido)

pedido.siguiente_estado()
print(pedido)

pedido.siguiente_estado()
print(pedido)

pedido.siguiente_estado()
print(pedido)

pedido.siguiente_estado()
print(pedido)

pedido.siguiente_estado()
print(pedido)  # Intentar avanzar más allá del estado final
