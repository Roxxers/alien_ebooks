FROM alien_ebooks:latest

# Need to quickly become root to install stuff to the container again

USER root

RUN apk add --no-cache npm &&\
    npm install typescript webpack webpack-cli ts-loader &&\
    npm cache clean --force

USER ebook