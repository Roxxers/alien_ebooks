FROM python:3.7.4-alpine
LABEL maintainer="me@roxxers.xyz"

# Copy home area and cd to new directory
COPY . /usr/src/app
WORKDIR /usr/src/app

# Setup OS
# Installing build-base to use gcc for psycopg2
# Installing libpq-postgresql-dev for support of postgres db's to install python libs
# Installing npm to get webpack for ts compiling

# Create user to run code from rather than root
# Make sure new user owns the app folder
# Install Python libs and compile Typescript files using webpack
# Then clean up files
RUN apk add --no-cache --update build-base postgresql-dev npm bash &&\
    adduser ebook --disabled-password --gecos "" &&\
    chown -R ebook /usr/src/app &&\
    npm install typescript webpack webpack-cli ts-loader &&\
    pip install pipenv --no-cache-dir &&\
    pipenv install --system --deploy --ignore-pipfile &&\
    npx webpack

# Become created user
USER ebook

# Command to run webapp
CMD ["python", "app.py"]
