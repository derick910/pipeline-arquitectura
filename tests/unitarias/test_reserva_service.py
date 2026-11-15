from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import pytest

from canchaya.reservas.aplicacion.servicio import ReservaService
from canchaya.reservas.dominio.modelos import (
    EstadoReserva,
    HorarioNoDisponible,
    RangoInvalido,
    ReservaNoEncontrada,
    TransicionInvalida,
)
from canchaya.reservas.infraestructura.memoria import RepositorioEnMemoria

INICIO = datetime(2026, 11, 20, 19, 0)
UNA_HORA = timedelta(hours=1)


@pytest.fixture
def servicio() -> ReservaService:
    return ReservaService(RepositorioEnMemoria())


def test_crea_reserva_pendiente(servicio):
    r = servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    assert r.estado == EstadoReserva.PENDIENTE


def test_rechaza_horario_solapado_en_la_misma_cancha(servicio):
    servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    with pytest.raises(HorarioNoDisponible):
        servicio.crear_reserva("c1", "u2", INICIO + timedelta(minutes=30), INICIO + 2 * UNA_HORA)


def test_permite_misma_hora_en_otra_cancha(servicio):
    servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    r = servicio.crear_reserva("c2", "u2", INICIO, INICIO + UNA_HORA)
    assert r.cancha_id == "c2"


def test_permite_horarios_contiguos(servicio):
    servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    r = servicio.crear_reserva("c1", "u2", INICIO + UNA_HORA, INICIO + 2 * UNA_HORA)
    assert r.estado == EstadoReserva.PENDIENTE


def test_rango_invalido(servicio):
    with pytest.raises(RangoInvalido):
        servicio.crear_reserva("c1", "u1", INICIO, INICIO)


def test_cancelar_libera_el_horario(servicio):
    r = servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    servicio.cancelar(r.id)
    nueva = servicio.crear_reserva("c1", "u2", INICIO, INICIO + UNA_HORA)
    assert nueva.estado == EstadoReserva.PENDIENTE


def test_confirmar_y_transiciones_invalidas(servicio):
    r = servicio.crear_reserva("c1", "u1", INICIO, INICIO + UNA_HORA)
    assert servicio.confirmar(r.id).estado == EstadoReserva.CONFIRMADA
    with pytest.raises(TransicionInvalida):
        servicio.confirmar(r.id)
    servicio.cancelar(r.id)
    with pytest.raises(TransicionInvalida):
        servicio.cancelar(r.id)


def test_reserva_inexistente(servicio):
    with pytest.raises(ReservaNoEncontrada):
        servicio.cancelar("no-existe")


def test_concurrencia_solo_una_reserva_por_horario(servicio):
    """RNF-04: ante intentos simultáneos, solo uno obtiene el horario."""

    def intentar(i: int) -> bool:
        try:
            servicio.crear_reserva("c1", f"u{i}", INICIO, INICIO + UNA_HORA)
            return True
        except HorarioNoDisponible:
            return False

    with ThreadPoolExecutor(max_workers=32) as pool:
        resultados = list(pool.map(intentar, range(1000)))
    assert sum(resultados) == 1
