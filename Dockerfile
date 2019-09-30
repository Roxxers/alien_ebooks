FROM python:3.7.4-alpine
LABEL maintainer="me@roxxers.xyz"

# Setting up vars

ENV USERNAME=sub
ENV FLASK_APP=subredditgenerator
ENV SUBREDDIT_USING_DOCKER=1
ENV INSTALL_DIR=/usr/src/app

# Setup OS
# Installing build-base to use gcc for psycopg2
# Installing libpq-dev for support of postgres db's to install python libs
# Installing node-typescript to install typescript complier so we can compile ts later on
RUN apk add --update build-base postgresql-dev npm 

# Install typescript

RUN npm i -g typescript && \
    npm cache clean --force
    
# Setup Env
# Create user to run code from rather than root
RUN adduser $USERNAME \
    --disabled-password \
    --gecos "" 

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
