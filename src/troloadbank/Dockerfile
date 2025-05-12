##==================================================================
##  Create a virtual environment with our app requirements
##==================================================================

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv/ /uvx/ /bin/

ENV APP_HOME="/opt/app/troloadbank"

WORKDIR $APP_HOME
COPY ./pyproject.toml . 

RUN uv lock --upgrade && \
    uv sync --no-dev  

##==================================================================
##  Build an image for our application invluding the pre-built env
##==================================================================

FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y sudo && \
    apt-get install -y iproute2 && \
    apt-get install -y nfs-common && \
    rm -rf /var/lib/apt/lists/*
# .     apt-get install -y --no-install-recommends sudo \
    #  apt-get install -y showmount && \

##  Create user with no privlages so we dont run as root
RUN groupadd -g 10000 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash -p $(openssl passwd appuser) appuser && \
    useradd -u 10003 -g staff -m -s /bin/bash -p $(openssl passwd House!5) jeff && \
    usermod -aG sudo jeff && \
    echo "jeff ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers 
    
##  Copy the pre-built virtual environment to our image
COPY --chown=appuser:appgroup --from=builder $VIRTUAL_ENV/ $VIRTUAL_ENV/

##  Copy the application code to our image
COPY --chown=appuser:appgroup src/ $APP_HOME/src
COPY --chown=appuser:appgroup etc/ $APP_HOME/etc

##  Application data
## VOLUME $APP_HOME/stage

##  Run it
USER appuser
WORKDIR $APP_HOME

CMD ["/bin/bash"]
#  ENTRYPOINT [ "uv", "run", "src/troloadbank.py" ]
#  CMD ["-e", "devl"]
