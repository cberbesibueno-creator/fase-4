# GRUPO DE PROGRAMACION 237
# KAREN DANIELA OVIEDO GODOY
#
# MODULO 2 CLASE CLIENTE - KAREN OVIEDO


import re

from Entidad import Entidad


class Cliente(Entidad):
    """Representa un cliente registrado en Software FJ."""

    def __init__(self, nombre, identificacion, correo, telefono):
        """Inicializa un cliente con sus datos personales."""
        super().__init__()

        self._nombre = self._validar_nombre(nombre)
        self._identificacion = self._validar_identificacion(identificacion)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)

    # Validaciones de los datos del cliente

    def _validar_nombre(self, nombre):
        """Comprueba que el nombre tenga un formato válido."""

        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser texto.")

        nombre = nombre.strip()

        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")

        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$"

        if not re.fullmatch(patron, nombre):
            raise ValueError("El nombre contiene caracteres no permitidos.")

        return nombre

    def _validar_identificacion(self, identificacion):
        """Comprueba que la identificación sea válida."""

        if not isinstance(identificacion, str):
            raise ValueError("La identificación debe ser texto.")

        identificacion = identificacion.strip()

        if not identificacion:
            raise ValueError("La identificación no puede estar vacía.")

        if not identificacion.isdigit():
            raise ValueError("La identificación solo debe contener números.")

        return identificacion

    def _validar_correo(self, correo):
        """Comprueba que el correo tenga un formato válido."""

        if not isinstance(correo, str):
            raise ValueError("El correo debe ser texto.")

        correo = correo.strip()

        if not correo:
            raise ValueError("El correo no puede estar vacío.")

        patron = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}$"

        if not re.fullmatch(patron, correo):
            raise ValueError("El correo electrónico no tiene un formato válido.")

        return correo

    def _validar_telefono(self, telefono):
        """Comprueba que el teléfono tenga un formato válido."""

        if not isinstance(telefono, str):
            raise ValueError("El teléfono debe ser texto.")

        telefono = telefono.strip()

        if not telefono:
            raise ValueError("El teléfono no puede estar vacío.")

        if not telefono.isdigit():
            raise ValueError("El teléfono solo debe contener números.")

        if not 7 <= len(telefono) <= 15:
            raise ValueError("El teléfono debe tener entre 7 y 15 dígitos.")

        return telefono

    # Propiedades de los atributos

    @property
    def nombre(self):
        """Permite consultar el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Modifica el nombre previa validación."""
        self._nombre = self._validar_nombre(nuevo_nombre)

    @property
    def identificacion(self):
        """Permite consultar la identificación del cliente."""
        return self._identificacion

    @property
    def correo(self):
        """Permite consultar el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo):
        """Modifica el correo previa validación."""
        self._correo = self._validar_correo(nuevo_correo)

    @property
    def telefono(self):
        """Permite consultar el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        """Modifica el teléfono previa validación."""
        self._telefono = self._validar_telefono(nuevo_telefono)

    # Descripción de la entidad

    def describir(self) -> str:
        """Devuelve una descripción de los datos del cliente."""

        return (
            f"Cliente: {self._nombre}\n"
            f"Identificación: {self._identificacion}\n"
            f"Correo: {self._correo}\n"
            f"Teléfono: {self._telefono}"
        )


