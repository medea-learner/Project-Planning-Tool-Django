FROM python:3.9.7-bullseye

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# root directory for the project
RUN mkdir /workspace

# Set the working directory
WORKDIR /workspace

# Copy the current directory contents into the container at /workspace
ADD . /workspace/

# For postgres db
RUN apt-get update && apt-get install -y libpq-dev

RUN pip install -r requirements.txt
