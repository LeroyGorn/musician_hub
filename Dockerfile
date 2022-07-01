FROM python:3.10

RUN apt update
RUN python --version

RUN mkdir /musician_hub

WORKDIR /musician_hub

COPY ./src ./src
COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "src/manage.py", "runserver", "0:8008"]