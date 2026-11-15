"""Casos de uso de reservas."""
from __future__ import annotations

import uuid
from datetime import datetime

from canchaya.reservas.dominio.modelos import (
    HorarioNoDisponible,
    Reserva,
    ReservaNoEncontrada,
)
from canchaya.reservas.dominio.puertos import ReservaRepository


class ReservaService:
    def __init__(self, repositorio: ReservaRepository) -> None:
        self._repo = repositorio

    def crear_reserva(
        self, cancha_id: str, cliente_id: str, inicio: datetime, fin: datetime
    ) -> Reserva:
        reserva = Reserva(str(uuid.uuid4()), cancha_id, cliente_id, inicio, fin)
        if not self._repo.agregar_si_libre(reserva):
            raise HorarioNoDisponible("El horario ya está reservado")
        return reserva

    def confirmar(self, id_reserva: str) -> Reserva:
        reserva = self._obtener(id_reserva)
        reserva.confirmar()
        return reserva

    def cancelar(self, id_reserva: str) -> Reserva:
        reserva = self._obtener(id_reserva)
        reserva.cancelar()
        return reserva

    def _obtener(self, id_reserva: str) -> Reserva:
        reserva = self._repo.buscar_por_id(id_reserva)
        if reserva is None:
            raise ReservaNoEncontrada(id_reserva)
        return reserva
