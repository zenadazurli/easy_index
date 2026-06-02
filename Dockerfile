FROM python:3.12-slim

# Installa uv e browser-use
RUN pip install uv
RUN uv pip install --system browser-use
RUN uvx browser-use install

WORKDIR /app

# Copia lo script
COPY get_indices.py .

# Attendi che il browser-use cloud sia pronto
RUN echo "Installazione completata"

# Comando di avvio (con timeout maggiore)
CMD ["python", "-u", "get_indices.py"]
