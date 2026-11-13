"""Módulo de cálculo métodos sobrecargados para Software FJ.
Implementa variantes de cálculo de costos con impuestos, descuentos, cargos
adicionales y sobrecarga por tipo de parámetro, garantizando tolerancia a
fallos y auditoría en archivo de logs.
"""

from functools import singledispatchmethod
import logging
from pathlib import Path
from typing import Any, Optional, Union, overload


class SoftwareFJError(Exception):
    """Esta es la base para errores controlados del sistema Software FJ."""


class DatosInvalidosError(SoftwareFJError):
    """Se utiliza cuando los valores de entrada son inválidos."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se utiliza cuando las reglas, cuando salen valores incoherentes."""
