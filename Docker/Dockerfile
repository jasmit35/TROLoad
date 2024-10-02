#  Starting image
FROM python:3.12-slim-bookworm as builder

#  Useful variables
ENV APP_NAME=troload
ENV APP_HOME=/opt/app/$APP_NAME
ARG APP_SRC="../src/$APP_NAME"

#  Update to stay secure
RUN apt-get -y update && apt-get -y upgrade

#  Change the working directory to the application home 
WORKDIR $APP_HOME 

#  Add the application code
ADD . . 

#  Check results
CMD ["/bin/bash"]
