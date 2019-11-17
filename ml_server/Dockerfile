# Dockerfile - this one for the ML server

# this file defines whats in the container

# build with docker build <path> -t <image_name>

# Pull base image, using an image with the cuda drivers installed - must match host drivers
FROM nvidia/cuda:10.1-base

# Set environment variables
# tells python not to make .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# stops docker from buffering python output
ENV PYTHONUNBUFFERED 1

#install python on this nvidia container as it is base environment
RUN apt-get update
RUN apt-get -y install python3.7 python3-pip

# Set work directory on the container
# this was required by the base image - details on hub.docker
WORKDIR /usr/src/app

# copy host: container ( i.e. into the workdir )
COPY requirements.txt ./

#install requirements inc pytorch and fastai
RUN pip3 install --no-cache-dir -r requirements.txt

# copy all other files in this directory to the work dir, inc the model
COPY . .

# run this file
CMD [ "python3", "api_server.py" ]