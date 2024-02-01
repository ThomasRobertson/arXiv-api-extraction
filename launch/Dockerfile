FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip --version  \
    && python --version  \
    && pip install -r requirements.txt

COPY init_app.sh init_app.sh

RUN chmod +x init_app.sh