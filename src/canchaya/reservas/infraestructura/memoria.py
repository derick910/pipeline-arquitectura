"""Repositorio en memoria: sirve para pruebas y para el componente mínimo."""
from __future__ import annotations

import threading
from typing import Dict, Optional

from canchaya.reservas.dominio.modelos import Reserva


class RepositorioEnMemoria:
    def __init__(self) -> None:
        self._reservas: Dict[str, Reserva] = {}
        self._lock = threading.Lock()

    def agregar_si_libre(self, reserva: Reserva) -> bool:
        with self._lock:
            for existente in self._reservas.values():
                if existente.activa and existente.solapa_con(reserva):
                    return False
            self._reservas[reserva.id] = reserva
            return True

    def buscar_por_id(self, id_reserva: str) -> Optional[Reserva]:
        return self._reservas.get(id_reserva)
