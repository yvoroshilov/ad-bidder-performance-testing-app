FROM python:3.11

WORKDIR /ad_publisher

COPY ./requirements.txt /ad_publisher/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ad_publisher/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
