
# GRUPO DE PROGRAMACION 237
# KAREN DANIELA OVIEDO GODOY
#
# ARCHIVO DE PRUEBAS - CLASE RESERVA


from Cliente import Cliente
from Reserva import Reserva


# Objeto provisional para representar un servicio.
class ServicioPrueba:
    """Representa un servicio temporal para las pruebas."""

    def __str__(self):
        return "Alquiler de equipos"


# Crea los objetos necesarios para realizar las pruebas.
cliente = Cliente(
    "María José",
    "1098765432",
    "maria@gmail.com",
    "3001234567"
)

servicio = ServicioPrueba()


# Crea una reserva con una duración válida.
reserva = Reserva(cliente, servicio, 3, "horas")


# Muestra la información inicial de la reserva.
print("=== INFORMACIÓN DE LA RESERVA ===")
print(reserva.describir())


# Comprueba la confirmación de la reserva.
print("\n=== CONFIRMACIÓN ===")
print(reserva.confirmar())
print("Estado actual:", reserva.estado)


# Comprueba el procesamiento de la reserva.
print("\n=== PROCESAMIENTO ===")
print(reserva.procesar())
print("Estado actual:", reserva.estado)


# Comprueba que no se pueda procesar una reserva dos veces.
print("\n=== PRUEBA DE ERROR: PROCESAMIENTO REPETIDO ===")

try:
    reserva.procesar()
except ValueError as error:
    print("Error controlado:", error)


# Comprueba que no se pueda cancelar una reserva procesada.
print("\n=== PRUEBA DE ERROR: CANCELACIÓN ===")

try:
    reserva.cancelar()
except ValueError as error:
    print("Error controlado:", error)


# Comprueba las validaciones de los datos de la reserva.
print("\n=== PRUEBAS DE VALIDACIÓN ===")

# Duración negativa.
try:
    Reserva(cliente, servicio, -3, "horas")
except ValueError as error:
    print("Duración negativa:", error)

# Duración con un tipo de dato incorrecto.
try:
    Reserva(cliente, servicio, "tres", "horas")
except ValueError as error:
    print("Duración no numérica:", error)

# Unidad de duración no permitida.
try:
    Reserva(cliente, servicio, 3, "semanas")
except ValueError as error:
    print("Unidad incorrecta:", error)

# Duración igual a cero.
try:
    Reserva(cliente, servicio, 0, "días")
except ValueError as error:
    print("Duración igual a cero:", error)

