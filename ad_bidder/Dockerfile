FROM python:3.11

WORKDIR /ad_bidder

COPY ./requirements.txt /ad_bidder/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /ad_bidder/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
