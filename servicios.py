from abc import abstractmethod
from entidades import Entidad, DatosInvalidosError, ServicioNoDisponibleError


class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser un número mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):
        pass

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")
        self.capacidad = capacidad

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        subtotal = self._tarifa_base * duracion
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_dia, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("Las unidades deben ser un entero positivo.")
        self.unidades = unidades

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, cantidad=1):
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > self.unidades:
            raise DatosInvalidosError("La cantidad solicitada supera las unidades disponibles.")
        subtotal = self._tarifa_base * duracion * cantidad
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Equipo: {self.nombre} | Unidades disponibles: {self.unidades}"


class Asesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Debe indicar la especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, tarifa_especial=0):
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        if tarifa_especial < 0:
            raise DatosInvalidosError("La tarifa especial no puede ser negativa.")
        tarifa = tarifa_especial if tarifa_especial > 0 else self._tarifa_base
        return round(tarifa * duracion * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad}"


def _validar_calculo(duracion, impuesto, descuento):
    if not isinstance(duracion, (int, float)) or duracion <= 0:
        raise DatosInvalidosError("La duración debe ser un número mayor que cero.")
    if not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
        raise DatosInvalidosError("El impuesto debe estar entre 0 y 1.")
    if not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
        raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")
