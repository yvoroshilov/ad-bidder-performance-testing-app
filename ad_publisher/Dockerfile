FROM python:3.11

ARG workdir_host=./ad_publisher
ARG workdir_container=/ad_publisher
ARG common_host=./common
ARG common_container=/common

WORKDIR $workdir_container

COPY $workdir_host/requirements.txt $workdir_container/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $workdir_container/requirements.txt

COPY $common_host $common_container
RUN pip install -e $common_container

CMD ["uvicorn", "ad_publisher.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--app-dir", "/ad_publisher/src"]
