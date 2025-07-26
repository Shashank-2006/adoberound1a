FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -m nltk.downloader punkt averaged_perceptron_tagger stopwords

COPY . .

RUN mkdir -p /app/input /app/output

ENTRYPOINT ["python3", "run_batch.py"]
