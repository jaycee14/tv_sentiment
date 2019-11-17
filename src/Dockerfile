# Dockerfile

# this file defines whats in the container

# build with docker build <path> -t <image_name>

# Pull base image
FROM python:3.7

# Set environment variables
# tells python not to makte .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# stops docker from buffering python output
ENV PYTHONUNBUFFERED 1

# Set work directory on the container
# this was required by the base image - details on hub.docker
WORKDIR /usr/src/app

# copy host: container ( i.e. into the workdir )
COPY requirements.txt ./

#install requirements
RUN pip install --no-cache-dir -r requirements.txt

# copy all other files in this directory to the work dir
COPY . .

# run this file
CMD [ "python", "app.py" ]