FROM python:alpine3.15
LABEL maintainer="pasharick@gmail.com"

WORKDIR /usr/src/app/backend

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /usr/src/app

ENTRYPOINT ["python", "bulls_cows.py"]

EXPOSE 5000

VOLUME /usr/src/app/dir_db