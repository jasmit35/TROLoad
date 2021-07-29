FROM python:3.9-slim-buster

COPY install-packages.sh .
RUN ./install-packages.sh

WORKDIR /home/container/troload
COPY ./src .

RUN useradd -m -d /home/container -u 5000 container 
RUN chown -R container /home/container

USER container

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT [ "python", "-u", "./local/python/troload.py" ]
