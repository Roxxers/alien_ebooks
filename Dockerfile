FROM python:3.7.4-buster
LABEL maintainer="me@roxxers.xyz"

# Setting up vars

ENV USERNAME=sub
ENV FLASK_APP=subredditgenerator
ENV SUBREDDIT_USING_DOCKER=1
ENV INSTALL_DIR=/usr/src/app

# Setup OS
# Installing libpq-dev for support of postgres db's to install python livs
# Installing node-typescript to install typescript complier so we can compile ts later on
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends libpq-dev node-typescript
# Clean the cache and apt lists to save space in the image
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Setup Env
# Create user to run code from rather than root
RUN useradd --shell /bin/bash $USERNAME

# Then copy source to home area and cd there
COPY . $INSTALL_DIR
WORKDIR $INSTALL_DIR

# Make sure new user owns the app folder
RUN chown -R $USERNAME $INSTALL_DIR

# Install Python libs and compile Typescript
RUN pip install --no-cache-dir -r requirements.txt
RUN tsc

# Become created user
USER $USERNAME

# Command to run webapp
CMD ["python3", "app.py"]
