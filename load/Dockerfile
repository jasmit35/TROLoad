FROM python:3.9-slim-buster

COPY install-packages.sh .
RUN ./install-packages.sh

RUN useradd -m -d /home/container -u 5000 container 
USER container
RUN mkdir /home/container/troload
WORKDIR /home/container/troload

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src .

CMD [ "python", "-u", "./local/python/troload.py", "-e", "$ENVIRONMENT" ]
 
