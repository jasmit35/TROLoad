#  Use the offical slim version of python as the base for our image
FROM python:3.8-slim

#  Set the working directory in the container
WORKDIR /code

#  Copy the dependiecies file from the source to the container working directory
COPY requirements.txt .

#  Install all the dependiences into the container
RUN pip install -r requirements.txt

#  Copy all the contents of the local src directory to the container 
COPY ./src /code


EXPOSE 5000
CMD python server.py
 