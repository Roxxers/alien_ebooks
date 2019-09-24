FROM python:3.7.4-buster
MAINTAINER Roxanne Gibson "me@roxxers.xyz"

# Setup OS
# requires lib-pq to be able to install dependancies
RUN apt-get update -y
RUN apt-get install -y libpq-dev

COPY . /usr/src/app
WORKDIR /usr/src/app 

ENV FLASK_APP=subredditgenerator
ENV SUBREDDIT_USING_DOCKER=1

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]