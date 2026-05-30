FROM python:3.12-slim

WORKDIR /app

COPY server.py .

RUN pip install fastapi uvicorn requests

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
