"""Módulo de cálculo con métodos sobrecargados para Software FJ.
Implementa variantes de cálculo de costos con impuestos, descuentos, cargos
adicionales y sobrecarga por tipo de parámetro, garantizando tolerancia a
fallos y auditoría en archivo de logs.
"""

from functools import singledispatchmethod
import logging
from pathlib import Path
from typing import Any, Optional, Union, overload


class SoftwareFJError(Exception):
    """Clase base para errores controlados del sistema Software FJ."""


class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los valores o tipos de entrada son inválidos."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando las reglas de negocio producen valores incoherentes."""


def configurar_logger_costos(ruta_log: Path = Path("logs/auditoria_costos.log")) -> logging.Logger:
    """Configura un logger dedicado con salida a archivo y consola."""
    ruta_log.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("SoftwareFJ.Costos")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        archivo_handler = logging.FileHandler(ruta_log, encoding="utf-8")
        archivo_handler.setFormatter(formato)
        consola_handler = logging.StreamHandler()
        consola_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)
        logger.addHandler(consola_handler)

    return logger


class CalculadoraCostosFJ:
    """Realiza los cálculos mediante métodos sobrecargados y despacho por tipo."""

    CUPONES_VALIDOS: dict[str, float] = {
        "BIENVENIDA10": 0.10,
        "CORPORATIVO15": 0.15,
        "VIP20": 0.20,
    }

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        self._logger = logger or configurar_logger_costos()

    # -------------------------------------------------------------------------
    # 1. SOBRECARGA POR FIRMA Y PARÁMETROS OPCIONALES (@overload)
    # -------------------------------------------------------------------------
    @overload
    def calcular_costo(self, costo_base: float) -> float: ...

    @overload
    def calcular_costo(self, costo_base: float, impuesto: float) -> float: ...

    @overload
    def calcular_costo(
        self,
        costo_base: float,
        impuesto: float,
        descuento: Optional[float],
    ) -> float: ...

    @overload
    def calcular_costo(
        self,
        costo_base: float,
        impuesto: float = 0.19,
        descuento: Optional[float] = None,
        cargo_adicional: float = 0.0,
    ) -> float: ...

    def calcular_costo(
        self,
        costo_base: float,
        impuesto: float = 0.19,
        descuento: Optional[float] = None,
        cargo_adicional: float = 0.0,
    ) -> float:
        """Calcula el costo total admitiendo múltiples combinaciones de parámetros.

        Variantes:
        - calcular_costo(base): aplica IVA estándar del 19 %.
        - calcular_costo(base, impuesto): aplica tasa impositiva personalizada.
        - calcular_costo(base, impuesto, descuento): aplica descuento porcentual + IVA.
        - calcular_costo(base, impuesto, descuento, cargo_adicional): incluye recargo fijo.
        """
        self._validar_numero_positivo(costo_base, "costo_base", permitir_cero=False)
        self._validar_rango_porcentaje(impuesto, "impuesto", maximo_inclusivo=True)
        self._validar_numero_positivo(cargo_adicional, "cargo_adicional", permitir_cero=True)

        porcentaje_desc = 0.0 if descuento is None else descuento
        self._validar_rango_porcentaje(porcentaje_desc, "descuento", maximo_inclusivo=False)

        subtotal = float(costo_base) + float(cargo_adicional)
        monto_descuento = subtotal * float(porcentaje_desc)
        base_gravable = subtotal - monto_descuento
        total = round(base_gravable * (1.0 + float(impuesto)), 2)

        if total <= 0:
            raise CalculoInconsistenteError("El total calculado debe ser mayor a cero.")

        self._logger.info(
            "Cálculo exitoso | Base: $%.2f | Cargo: $%.2f | Desc: %.0f%% | IVA: %.0f%% -> Total: $%.2f",
            costo_base,
            cargo_adicional,
            porcentaje_desc * 100,
            impuesto * 100,
            total,
        )
        return total

    # -------------------------------------------------------------------------
    # 2. SOBRECARGA POR TIPO DE ARGUMENTO (@singledispatchmethod)
    # -------------------------------------------------------------------------
    @singledispatchmethod
    def _aplicar_beneficio_dispatch(self, beneficio: Any, monto_base: float) -> float:
        """Sobrecarga dinámica según el tipo de beneficio recibido (float, int o str)."""
        raise DatosInvalidosError(
            f"Tipo de beneficio no soportado: '{type(beneficio).__name__}'. "
            "Use float (porcentaje), int (monto fijo) o str (código de cupón)."
        )

    def aplicar_beneficio(self, monto_base: float, beneficio: Any) -> float:
        """Aplica un beneficio sobre un monto base según el tipo del beneficio."""
        return self._aplicar_beneficio_dispatch(beneficio, monto_base)

    @_aplicar_beneficio_dispatch.register(float)
    def _(self, beneficio: float, monto_base: float) -> float:
        """Variante 1 (float): Aplica un descuento porcentual en el rango [0.0, 1.0)."""
        self._validar_numero_positivo(monto_base, "monto_base", permitir_cero=False)
        self._validar_rango_porcentaje(beneficio, "beneficio porcentual", maximo_inclusivo=False)
        resultado = round(monto_base * (1.0 - beneficio), 2)
        self._logger.info("Beneficio porcentual (%.0f%%) aplicado -> $%.2f", beneficio * 100, resultado)
        return resultado

    @_aplicar_beneficio_dispatch.register(int)
    def _(self, beneficio: int, monto_base: float) -> float:
        """Variante 2 (int): Resta un bono fijo en pesos al monto base."""
        if isinstance(beneficio, bool):
            raise DatosInvalidosError("Un valor booleano no es un bono monetario válido.")
        self._validar_numero_positivo(monto_base, "monto_base", permitir_cero=False)
        if beneficio < 0 or beneficio >= monto_base:
            raise CalculoInconsistenteError(
                f"El bono fijo (${beneficio}) debe ser >= 0 y menor al monto base (${monto_base})."
            )
        resultado = round(float(monto_base - beneficio), 2)
        self._logger.info("Bono fijo ($%d) aplicado -> $%.2f", beneficio, resultado)
        return resultado

    @_aplicar_beneficio_dispatch.register(str)
    def _(self, beneficio: str, monto_base: float) -> float:
        """Variante 3 (str): Valida un código promocional y aplica su tasa asociada."""
        self._validar_numero_positivo(monto_base, "monto_base", permitir_cero=False)
        codigo = beneficio.strip().upper()
        if codigo not in self.CUPONES_VALIDOS:
            raise DatosInvalidosError(f"El cupón '{beneficio}' no existe o ha expirado.")
        tasa = self.CUPONES_VALIDOS[codigo]
        resultado = round(monto_base * (1.0 - tasa), 2)
        self._logger.info("Cupón '%s' (%.0f%%) aplicado -> $%.2f", codigo, tasa * 100, resultado)
        return resultado

    # -------------------------------------------------------------------------
    # VALIDACIONES INTERNAS
    # -------------------------------------------------------------------------
    @staticmethod
    def _validar_numero_positivo(valor: Union[int, float], nombre: str, permitir_cero: bool) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(f"El parámetro '{nombre}' debe ser numérico.")
        if permitir_cero and valor < 0:
            raise CalculoInconsistenteError(f"El parámetro '{nombre}' no puede ser negativo.")
        if not permitir_cero and valor <= 0:
            raise CalculoInconsistenteError(f"El parámetro '{nombre}' debe ser mayor a cero.")

    @staticmethod
    def _validar_rango_porcentaje(valor: Union[int, float], nombre: str, maximo_inclusivo: bool) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatosInvalidosError(f"El parámetro '{nombre}' debe ser numérico.")
        limite_ok = (0.0 <= valor <= 1.0) if maximo_inclusivo else (0.0 <= valor < 1.0)
        if not limite_ok:
            rango = "[0.0, 1.0]" if maximo_inclusivo else "[0.0, 1.0)"
            raise CalculoInconsistenteError(f"El parámetro '{nombre}' debe estar en {rango}.")


if __name__ == "__main__":
    calc = CalculadoraCostosFJ()

    # Pruebas de sobrecarga por parámetros opcionales (@overload)
    print("1. Solo base + IVA 19%:", calc.calcular_costo(200000.0))
    print("2. Base + IVA 0%:", calc.calcular_costo(200000.0, 0.0))
    print("3. Base + IVA 19% + Desc 10%:", calc.calcular_costo(200000.0, 0.19, 0.10))
    print("4. Completa + Cargo $30k:", calc.calcular_costo(200000.0, 0.19, 0.10, 30000.0))

    # Pruebas de sobrecarga por tipo de argumento (@singledispatchmethod)
    print("5. Descuento float (15%):", calc.aplicar_beneficio(200000.0, 0.15))
    print("6. Bono fijo int ($25,000):", calc.aplicar_beneficio(200000.0, 25000))
    print("7. Cupón str ('VIP20'):", calc.aplicar_beneficio(200000.0, "VIP20"))

    # Prueba de tolerancia a fallos
    try:
        calc.aplicar_beneficio(200000.0, [10, 20])
    except SoftwareFJError as err:
        print("8. Error controlado capturado:", err)