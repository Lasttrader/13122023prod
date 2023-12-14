FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /flaskApp
WORKDIR /flaskApp
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
