FROM python:3.11-slim-bullseye
LABEL authors="Arturo Ortiz"

WORKDIR /app

EXPOSE 8501
EXPOSE 8888

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter

COPY . /app

#RUN python -m pytest -p no:warnings

ENTRYPOINT ["sh", "-c", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --ServerApp.token='' --ServerApp.password='' --ServerApp.allow_origin='*' & streamlit run main.py --server.port=8501 --server.address=0.0.0.0"]