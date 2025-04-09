FROM python:3.11-slim

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto para instalar dependencias
COPY pyproject.toml poetry.lock* ./

# Configurar Poetry para que NO cree entornos virtuales dentro del contenedor
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --only main --no-root

# Copiar el código fuente (por ahora solo `main.py`, pero mejor copiar todo si usas más archivos luego)
COPY . .

# Exponer el puerto que usará FastAPI (útil si necesitas depurar desde fuera del contenedor)
EXPOSE 8001

# Comando para iniciar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
