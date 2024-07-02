FROM python:3.10.14-alpine3.20
WORKDIR /main


COPY requirements.txt .

RUN pip install -r requirements.txt
   


COPY . .


CMD ["python", "executer.py"]