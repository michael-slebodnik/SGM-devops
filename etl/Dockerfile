FROM python:3.8

WORKDIR /app/etl
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "etl.py"]
