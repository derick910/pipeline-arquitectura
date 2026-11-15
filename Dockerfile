FROM python:3.12-slim AS base
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
RUN useradd --uid 1001 --no-create-home appuser
USER 1001
CMD ["python", "-c", "import canchaya; print('CanchaYa listo')"]
