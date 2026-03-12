FROM python:3.10-slim

WORKDIR /app

# install curl for healthcheck
RUN apt-get update && apt-get install -y curl

COPY requirements.txt .

# upgrade pip
RUN pip install --upgrade pip

# install torch separately (cached layer)
RUN pip install torch==2.4.0 --index-url https://download.pytorch.org/whl/cpu

# install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]