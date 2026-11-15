# CanchaYa: componente mínimo de reservas

Componente de ejemplo del Proyecto Final de Arquitectura de Software.
Implementa la regla central (sin dobles reservas) con arquitectura en capas.

## Ejecutar las pruebas
```bash
pip install -e ".[dev]"
ruff check src tests
pytest --cov=canchaya --cov-report=term-missing --cov-fail-under=80
```

## Estructura
- `src/canchaya/reservas/dominio`: entidades, reglas y puertos (sin dependencias externas).
- `src/canchaya/reservas/aplicacion`: casos de uso (`ReservaService`).
- `src/canchaya/reservas/infraestructura`: repositorio en memoria.
- `tests/unitarias`, `tests/arquitectura`: pruebas.
- `.github/workflows/ci.yml`: pipeline de CI en GitHub Actions.
