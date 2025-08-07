FROM python:3.11-slim

# 1. Set working directory and unbuffered output
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# 2. Install system-level deps in one layer
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       gcc \
       g++ \
       curl \
  && rm -rf /var/lib/apt/lists/*

# 3. Upgrade pip
RUN pip install --upgrade pip

# 4. Install CPU-only PyTorch & Torchvision  
RUN pip install \
    --index-url https://download.pytorch.org/whl/torch_stable.html \
    torch==2.1.0+cpu \
    torchvision==0.16.0+cpu

# 5. Copy requirements and install all other Python deps  
#    (Ensure torch & torchvision are NOT in requirements.txt)
COPY requirements.txt .
RUN pip install --no-deps -r requirements.txt

# 6. Copy your application code  
#    (now that deps are in place, code changes won’t bust the cache)
COPY . .

# 7. Create uploads dir (if your app writes to it at runtime)
RUN mkdir -p uploads

# 8. Env var, port, healthcheck
ENV PORT=8080
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# 9. Entry point
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
