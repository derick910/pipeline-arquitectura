"""Fitness function: el dominio no debe importar capas externas (sección 3.2)."""
import ast
from pathlib import Path

DOMINIO = Path(__file__).resolve().parents[2] / "src/canchaya/reservas/dominio"
PROHIBIDOS = (
    "canchaya.reservas.aplicacion",
    "canchaya.reservas.infraestructura",
    "fastapi",
    "sqlalchemy",
    "psycopg",
    "redis",
)


def _importaciones(archivo: Path):
    arbol = ast.parse(archivo.read_text(encoding="utf-8"))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            yield from (a.name for a in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            yield nodo.module


def test_dominio_no_depende_de_infraestructura_ni_frameworks():
    infracciones = [
        (a.name, m)
        for a in DOMINIO.glob("*.py")
        for m in _importaciones(a)
        if m.startswith(PROHIBIDOS)
    ]
    assert infracciones == []
