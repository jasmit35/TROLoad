##=============================================================================================
##  Create a virtual environment with our app requirements
##=============================================================================================

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv/ /uvx/ /bin/

ENV APP_HOME="/opt/app/troloadbank"

WORKDIR $APP_HOME
COPY ./pyproject.toml . 

RUN uv lock --upgrade && \
    uv sync --no-dev  

##=============================================================================================
##  Build an image for our application including the pre-built venv
##=============================================================================================

FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

##  --------------------------------------------------------------------------------------------
##  Environment varables for build and inside container 

ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

##  --------------------------------------------------------------------------------------------
##  Add addition software and upgrade all to current

RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y iproute2 && \
    apt-get install -y nfs-common && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

##  --------------------------------------------------------------------------------------------
##  Application and my userid 

RUN groupadd -g 10000 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash \
            -p $(openssl passwd appuser) appuser && \
    useradd -u 10003 -g staff -m -s /bin/bash \
            -p $(openssl passwd jeff) jeff && \
    usermod -aG sudo jeff && \
    echo "jeff ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers 

    
##  --------------------------------------------------------------------------------------------
##  Copy pre-built virtual environment to image

COPY --chown=appuser:appgroup --from=builder $VIRTUAL_ENV/ $VIRTUAL_ENV/

##  --------------------------------------------------------------------------------------------
##  Copy application code to image

COPY --chown=appuser:appgroup src/ $APP_HOME/src
COPY --chown=appuser:appgroup etc/ $APP_HOME/etc

##  --------------------------------------------------------------------------------------------
##  Application data

RUN ln -s /mnt/nfsstorage/TROLoad/stage $APP_HOME/stage

##  --------------------------------------------------------------------------------------------
##  Run app via uv 

USER appuser
WORKDIR $APP_HOME
CMD ["/bin/bash"]
#  ENTRYPOINT [ "uv", "run", "src/troloadbank.py" ]
#  CMD ["-e", "devl"]
