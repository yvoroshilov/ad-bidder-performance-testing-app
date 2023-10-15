FROM python:3.11

ARG src_host=./ad_publisher
ARG src_container=/ad_publisher
ARG common_host=./common
ARG common_container=/common

WORKDIR $src_container

COPY $src_host/requirements.txt $src_container/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $src_container/requirements.txt

COPY $common_host $common_container
RUN pip install -e $common_container

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
