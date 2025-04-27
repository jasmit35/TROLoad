##==================================================================
##  Create a virtual environment with our app requirements
##==================================================================

FROM python:3.12 AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

ENV APP_HOME="/opt/app/troloadbank"

WORKDIR $APP_HOME
COPY ./pyproject.toml ./uv.lock . 
# COPY ./src/troloadbank/wheels/ $APP_HOME/wheels/ 

RUN uv sync --locked

##==================================================================
##  Build an image for our application invluding the pre-built env
##==================================================================

FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.16 /uv /uvx /bin/

ENV APP_NAME="troloadbank"
ENV APP_HOME="/opt/app/$APP_NAME"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && \
    apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

##  Create user with no privlages so we dont run as root
RUN groupadd -g 10000 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

##  Copy the pre-built virtual environment to our image
COPY --chown=appuser:appgroup --from=builder $VIRTUAL_ENV/ $VIRTUAL_ENV/

##  Copy the application code to our image
COPY --chown=appuser:appgroup src/ $APP_HOME/src
# COPY --chown=appuser:appgroup wheels/ $APP_HOME/wheels

##  Run it
USER appuser
WORKDIR $APP_HOME

#  CMD ["/bin/bash"]
#  ENTRYPOINT [ "python", "/src/troloadbank.py" ]
#  CMD ["-e", "devl"]
ENTRYPOINT [ "uv", "run", "src/troloadbank.py" ]
CMD ["-e", "devl"]
