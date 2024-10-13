#================================================================== 
#  Part 1:
#  Build a virtual environment with all of 
#  our requirements except the application.
#================================================================== 

# syntax=docker/dockerfile:1

FROM python:3.12 AS builder

#  Install the uv utility
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

#  Copy in the project file
RUN mkdir -p /opt/app/troload 
WORKDIR /opt/app/troload
COPY pyproject.toml . 

#  Use uv to create the virtual environment with all requirements
RUN uv sync

##================================================================== 
##  Part 2:
##  Copy in our pre-built virtual environment and activate it.
##  Copy in our applicaion.
##================================================================== 

FROM python:3.12-slim-bookworm

ENV VIRTUAL_ENV="/opt/app/troload/.venv"
ENV APP_HOME="/opt/app/troload"

#  Create a container id to run the app
RUN groupadd -g 10001 container && \
    useradd -u 10000 -g container container

#  Get any updates and instll other necessities
RUN apt-get -y update && \
    apt-get -y upgrade

#  Copy the virtual environment with all our requiements and activate
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV 
COPY ./src /opt/app
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN chown -R container:container $APP_HOME 
WORKDIR $APP_HOME 
USER container:container

#  Copy in our application and run it
ENTRYPOINT ["python", "/opt/app/troload/python/troload.py"]
CMD ["-e", "devl", "-t", "cat"]

#  CMD ["/bin/bash"]
