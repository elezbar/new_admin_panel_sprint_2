FROM python:3.10.8
# Slim версия не содержит достаточного количества элемнтов необходимых для работы некоторых библиотек из списка

WORKDIR /opt/app


COPY requirements.txt requirements.txt

RUN  mkdir -p /opt/app/static/ \
     && mkdir -p /opt/app/media/ \
     && pip install --no-cache-dir --upgrade pip==22.3\ 
     && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 config.wsgi

