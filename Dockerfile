#==================================================================
#  Part 1:
#  Build a virtual environment with all of
#  our requirements except the application.
#==================================================================

# SYNTAX=docker/dockerfile:1
FROM python:3.12 AS builder

#  Install the uv utility
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

#  Install a virtual environment
ENV APP_HOME="/opt/app/troloadtrans"
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

#  Set up the project file
COPY pyproject.toml uv.lock .
RUN uv venv --python=3.12 $APP_HOME/.venv

#  RUN uv lock
#  RUN uv pip install psycopg2-binary openpyxl

##==================================================================
##  Part 2:
##  Copy in our pre-built virtual environment and activate it.
##  Copy in our applicaion.
##==================================================================

FROM python:3.12-slim-bookworm

#  Get any updates
RUN apt-get -y update && \
    apt-get -y upgrade

#  Copy the pre-built virtual environment and the application code
ENV APP_HOME="/opt/app/troloadtrans"
ENV VIRTUAL_ENV="$APP_HOME/.venv"
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#  Install the uv utility
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
RUN uv pip install psycopg2-binary openpyxl pandas

#  Create an id to run the app
RUN groupadd -g 10000 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

COPY ./src /opt/app
RUN chown -R appuser:appgroup $APP_HOME
WORKDIR $APP_HOME
USER appuser

#  Run it
ENTRYPOINT ["python", "/opt/app/troloadtrans/python/troloadtrans.py"]
CMD ["-e", "devl"]
