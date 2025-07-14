##=============================================================================================
##  Create a virtual environment with our app requirements
##=============================================================================================

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv/ /uvx/ /bin/

##  Environment varables for the build
ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"

##  Create app directory and set as pwd
WORKDIR $APP_HOME

##  Copy the project file then use uv to create a venv and install deps
COPY ./pyproject.toml .
RUN uv lock --upgrade && \
    uv sync --no-dev

##=============================================================================================
##  Build an image for our application including the pre-built venv
##=============================================================================================

FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

##  Environment varables for build and inside container
ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

##  Add additional software and upgrade all to current
RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y iproute2 && \
    apt-get install -y nfs-common && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

##  Set the timezone
RUN ln -sf /usr/share/zoneinfo/America/Chicago /etc/localtime && \
    echo "America/Chicago" > /etc/timezone

##  Application and my userid
RUN groupadd -g 20000 appgroup && \
    useradd -u 20002 -g appgroup -m -s /bin/bash -p $(openssl passwd appuser) appuser && \
    groupadd -g 10000 jeff && \
    useradd -u 10000 -g jeff -m -s /bin/bash -p $(openssl passwd jeff) jeff && \
    usermod -aG sudo jeff && \
    echo "jeff ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

##  Copy pre-built virtual environment to image
COPY --chown=appuser:appgroup --from=builder $VIRTUAL_ENV/ $VIRTUAL_ENV/

##  Copy the application to the image
COPY --chown=appuser:appgroup src/ $APP_HOME/

##  Set pwd and run as non-root user
WORKDIR $APP_HOME
USER appuser

##  Drop in to bash for interactive use
#  CMD ["/bin/bash"]

##  Run app via uv
ENTRYPOINT [ "uv", "run", "python/troloadbank.py" ]
#  CMD ["-e", "devl", "--cfgfile", "etc/troloadbank.cfg"]
