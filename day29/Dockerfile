# 1️⃣ Base image
FROM python:3.12-slim

# 2️⃣ Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory
WORKDIR /app

# 4️⃣ Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5️⃣ Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy application code
COPY . .

# 7️⃣ Expose FastAPI port
EXPOSE 8000

# 8️⃣ Run migrations + start server
CMD ["bash", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
