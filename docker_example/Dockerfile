FROM python:3.10

RUN apt update
RUN python --version

RUN mkdir /test_docker


WORKDIR /test_docker

COPY hello_docker.py ./hello_docker.py
COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "hello_docker.py"]
