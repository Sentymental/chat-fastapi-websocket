FROM python:3.10

WORKDIR /fastapi-chatapp

COPY . /

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app ./app

CMD ["python3", "./app/main.py"]
