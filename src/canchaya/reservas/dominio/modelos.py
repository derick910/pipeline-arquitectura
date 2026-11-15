"""Dominio de reservas: entidades, estados y errores (sin dependencias externas)."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EstadoReserva(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"


class ErrorDominio(Exception):
    """Error base de las reglas de negocio."""


class RangoInvalido(ErrorDominio):
    """El fin de la reserva no es posterior al inicio."""


class HorarioNoDisponible(ErrorDominio):
    """Existe otra reserva activa en la misma cancha y horario (RNF-04)."""


class TransicionInvalida(ErrorDominio):
    """La operación no está permitida en el estado actual."""


class ReservaNoEncontrada(ErrorDominio):
    """No existe una reserva con ese identificador."""


@dataclass
class Reserva:
    id: str
    cancha_id: str
    cliente_id: str
    inicio: datetime
    fin: datetime
    estado: EstadoReserva = EstadoReserva.PENDIENTE

    def __post_init__(self) -> None:
        if self.fin <= self.inicio:
            raise RangoInvalido("El fin debe ser posterior al inicio")

    @property
    def activa(self) -> bool:
        return self.estado != EstadoReserva.CANCELADA

    def solapa_con(self, otra: Reserva) -> bool:
        """Dos reservas se solapan si comparten cancha y sus rangos se cruzan."""
        return (
            self.cancha_id == otra.cancha_id
            and self.inicio < otra.fin
            and otra.inicio < self.fin
        )

    def confirmar(self) -> None:
        if self.estado != EstadoReserva.PENDIENTE:
            raise TransicionInvalida(f"No se puede confirmar una reserva {self.estado.value}")
        self.estado = EstadoReserva.CONFIRMADA

    def cancelar(self) -> None:
        if self.estado == EstadoReserva.CANCELADA:
            raise TransicionInvalida("La reserva ya está cancelada")
        self.estado = EstadoReserva.CANCELADA
