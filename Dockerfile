FROM python:3.12-alpine

WORKDIR /app

COPY ./src ./src
COPY ./requirments.txt .

RUN pip install -r requirments.txt

CMD ["python","./src/app.py"]