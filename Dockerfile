FROM python:3.7.4-buster
MAINTAINER Roxanne Gibson "me@roxxers.xyz"

# Setting up vars

ENV USERNAME=sub
ENV FLASK_APP=subredditgenerator
ENV SUBREDDIT_USING_DOCKER=1
ENV PATH=$PATH:$USERHOME/.local/bin

# Setup OS
RUN apt-get update -y
RUN apt-get install -y libpq-dev node-typescript
# Installing libpq-dev for support of postgres db's to install python livs
# Installing node-typescript to install typescript complier so we can compile ts later on

# Setup Env
# Create user to run code from rather than root
RUN useradd --shell /bin/bash $USERNAME

# Then copy source to home area and cd there
COPY . /usr/src/app
WORKDIR /usr/src/app

# Make sure new user owns the app folder
RUN chown -R $USERNAME /usr/src/app

# Install Python libs and compile Typescript
RUN pip install --no-cache-dir -r requirements.txt
RUN tsc

# Become created user
USER $USERNAME

# Command to run webapp
CMD ["python3", "app.py"]
