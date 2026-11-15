"""Puertos del dominio: interfaces que implementa la infraestructura."""
from __future__ import annotations

from typing import Protocol

from .modelos import Reserva


class ReservaRepository(Protocol):
    def agregar_si_libre(self, reserva: Reserva) -> bool:
        """Guarda la reserva solo si no se solapa con otra activa.

        Debe ser atómica. En producción la garantiza la restricción de
        exclusión de PostgreSQL (ADR-04).
        """

    def buscar_por_id(self, id_reserva: str) -> Reserva| None: ...
