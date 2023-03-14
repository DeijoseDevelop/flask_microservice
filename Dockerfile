# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /code
ENV FLASK_APP=./modular/flask_app/run.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN pip install cmake
# RUN pip install dlib
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 systemd -y
RUN ln -sfn /usr/share/zoneinfo/America/Bogota /etc/localtime
EXPOSE 5000
COPY . .
CMD ["flask", "run"]

