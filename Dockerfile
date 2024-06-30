FROM python:3.10.14-alpine3.20
WORKDIR /main


COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps


COPY . .


CMD ["python", "executer.py"]