# GRUPO DE PROGRAMACION 237
# KAREN DANIELA OVIEDO GODOY
#
# ARCHIVO DE PRUEBAS - CLASE CLIENTE

from Cliente import Cliente

try:
    cliente = Cliente(
        "María José",
        "1098765432",
        "maria@gmail.com",
        "3001234567"
    )

    print(cliente.describir())

    cliente.correo = "maria.nuevo@gmail.com"

    print("\nCorreo actualizado:", cliente.correo)

except ValueError as error:
    print("Error:", error)