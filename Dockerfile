FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV LIVING_AI_STORAGE_BACKEND=redis
ENV LIVING_AI_REDIS_URL=redis://redis:6379/0
ENV LIVING_AI_USE_QUEUE=1
ENV LIVING_AI_API_KEYS=demo-key

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
