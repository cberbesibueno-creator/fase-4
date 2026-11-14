# GRUPO DE PROGRAMACION 237
# KAREN DANIELA OVIEDO GODOY
#
# MODULO CLASE RESERVA - KAREN OVIEDO

from Entidad import Entidad
from Cliente import Cliente

class Reserva(Entidad):
    """Representa una reserva de un servicio en Software FJ."""

    def __init__(self, cliente, servicio, duracion, unidad_duracion):
        """Inicializa una reserva con sus datos principales."""

        # Comprueba que el cliente sea un objeto de la clase Cliente.
        if not isinstance(cliente, Cliente):
         raise ValueError("El cliente debe ser un objeto de la clase Cliente.")

        # Valida la duración y su unidad antes de crear la reserva.
        duracion = self._validar_duracion(duracion)
        unidad_duracion = self._validar_unidad(unidad_duracion)

        # Hereda de Entidad el identificador único de la reserva.
        super().__init__()

        # Almacena el cliente y el servicio asociados a la reserva.
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._unidad_duracion = unidad_duracion

        # Toda reserva comienza con estado pendiente.
        self._estado = "Pendiente"

    def _validar_duracion(self, duracion):
        """Comprueba que la duración sea un número positivo."""

        # Evita valores que no sean numéricos, incluyendo los booleanos.
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ValueError("La duración debe ser un valor numérico.")

        # La duración debe ser mayor que cero.
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        return duracion

    def _validar_unidad(self, unidad):
        """Comprueba que la unidad de duración sea válida."""

        # Verifica que la unidad recibida sea una cadena de texto.
        if not isinstance(unidad, str):
            raise ValueError("La unidad de duración debe ser texto.")

        # Elimina espacios y normaliza el texto a minúsculas.
        unidad = unidad.strip().lower()

        # Solo se permiten horas o días como unidades de duración.
        if unidad not in ("horas", "días"):
            raise ValueError("La unidad debe ser horas o días.")

        return unidad

    # Propiedades para consultar los datos de la reserva.

    @property
    def cliente(self):
        """Devuelve el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Devuelve el servicio asociado a la reserva."""
        return self._servicio

    @property
    def duracion(self):
        """Devuelve la duración de la reserva."""
        return self._duracion

    @property
    def unidad_duracion(self):
        """Devuelve la unidad de tiempo de la reserva."""
        return self._unidad_duracion

    @property
    def estado(self):
        """Devuelve el estado actual de la reserva."""
        return self._estado

    def confirmar(self):
        """Confirma una reserva que se encuentre pendiente."""

        # Comprueba que la reserva todavía pueda confirmarse.
        if self._estado != "Pendiente":
            raise ValueError(
                "Solo se pueden confirmar reservas pendientes."
            )

        # Actualiza el estado de la reserva.
        self._estado = "Confirmada"

        return "La reserva ha sido confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""

        # Comprueba que la reserva pueda ser cancelada.
        if self._estado not in ("Pendiente", "Confirmada"):
            raise ValueError(
                "Solo se pueden cancelar reservas pendientes o confirmadas."
            )

        # Actualiza el estado de la reserva.
        self._estado = "Cancelada"

        return "La reserva ha sido cancelada correctamente."

    def procesar(self):
        """Procesa una reserva que se encuentre confirmada."""

        # Comprueba que la reserva esté confirmada antes de procesarla.
        if self._estado != "Confirmada":
            raise ValueError(
                "Solo se pueden procesar reservas confirmadas."
            )

        # Actualiza el estado para indicar que la reserva fue procesada.
        self._estado = "Procesada"

        return "La reserva ha sido procesada correctamente."

    def describir(self):
        """Devuelve una descripción completa de la reserva."""

        # Organiza los datos principales de la reserva en un texto.
        return (
            f"Reserva N.° {self.id}\n"
            f"Cliente: {self._cliente.nombre}\n"
            f"Servicio: {self._servicio}\n"
            f"Duración: {self._duracion} {self._unidad_duracion}\n"
            f"Estado: {self._estado}"
        )
    