#==================================================================
#  Part 1:
#  Build a virtual environment with all of
#  our requirements except the application.
#==================================================================

# SYNTAX=docker/dockerfile:1

FROM python:3.12 AS builder

ENV APP_HOME="/opt/app/troload"

#  Install the uv utility
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

#  Set up the project file
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
COPY pyproject.toml .

#  Use uv to create the virtual environment with all
#  requirements for the app but none for development
RUN uv sync --no-dev

##==================================================================
##  Part 2:
##  Copy in our pre-built virtual environment and activate it.
##  Copy in our applicaion.
##==================================================================

FROM python:3.12-slim-bookworm

ENV APP_HOME="/opt/app/troload"
ENV VIRTUAL_ENV="/opt/app/troload/.venv"

#  Copy the pre-built virtual environment and the application code
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./src /opt/app

#  Get any updates
RUN apt-get -y update && \
    apt-get -y upgrade

#  Create a container id to run the app
RUN groupadd -g 10000 container && \
    useradd -u 10001 -g container container

RUN chown -R container:container $APP_HOME
WORKDIR $APP_HOME
USER container:container

#  Run it
ENTRYPOINT ["python", "/opt/app/troload/python/troload.py"]
CMD ["-e", "devl", "-t", "cat"]

#  CMD ["/bin/bash"]
