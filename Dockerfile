FROM python:3.9-slim-buster as base

COPY install-packages.sh .
RUN ./install-packages.sh

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /home/container/troload
COPY ./src .

RUN useradd -m -d /home/container -u 5000 container 
RUN chown -R container /home/container

###  Build debug image  ###
FROM base AS debug

USER container
RUN pip install debugpy

# ENTRYPOINT [ "python", "-u", "./local/python/troload.py" ]
# CMD python -m debugpy --host 0.0.0.0 --port 5678 python -u ./local/python/troload.py
ENTRYPOINT python -m debugpy host 0.0.0.0 --port 5678 python -u ./local/python/troload.py

###  Build production image  ###
FROM base AS prod 

USER container
ENTRYPOINT [ "python", "-u", "./local/python/troload.py" ]
