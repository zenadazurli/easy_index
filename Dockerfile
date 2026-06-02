FROM python:3.12-slim

RUN pip install uv
RUN uv pip install --system browser-use
RUN uvx browser-use install

WORKDIR /app
COPY get_indices.py .

CMD ["python", "get_indices.py"]
