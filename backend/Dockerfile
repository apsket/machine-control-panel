FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build deps and runtime deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
