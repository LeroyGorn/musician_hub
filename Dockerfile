FROM python:3.10

RUN apt update

RUN mkdir /musician_hub

WORKDIR /musician_hub

COPY ./src ./src

COPY ./commands/start_project.sh **/script**

COPY requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash", "./commands/start_project.sh"]
CMD ["bash"]
