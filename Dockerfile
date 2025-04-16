##==================================================================
##  Prepare the build environment
##==================================================================

# SYNTAX=docker/dockerfile:1
FROM python:3.12 AS builder

COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

##==================================================================
##  Create the virtual environment 
##==================================================================

ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"

WORKDIR $APP_HOME
COPY ./pyproject.toml ./uv.lock . 
RUN uv sync

##==================================================================
##  Build the base image for the application 
##==================================================================

FROM python:3.12-slim-bookworm

#  COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

RUN apt-get -y update && \
    apt-get -y upgrade

##==================================================================
##  Copy the pre-built virtual environment 
##==================================================================

ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

##==================================================================
##  Move the application code to the image
##==================================================================

RUN groupadd -g 10000 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

COPY src/$APP_NAME/ $APP_HOME/
RUN chown -R appuser:appgroup $APP_HOME
WORKDIR $APP_HOME
USER appuser

##==================================================================
##  Run it
##==================================================================

#  CMD ["/bin/bash"]
ENTRYPOINT [ "python", "python/troloadbank.py" ]
CMD ["-e", "devl"]
