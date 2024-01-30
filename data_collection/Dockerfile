FROM python:3.10

# set https_proxy if required (e.g. local PC in Germany)
ENV https_proxy="$https_proxy"

WORKDIR /app/data_collection
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
