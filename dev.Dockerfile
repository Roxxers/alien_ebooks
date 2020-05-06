FROM alien_ebooks:latest

# Need to quickly become root to install stuff to the container again

USER root

ENV NODE_ENV development

RUN apk add --no-cache npm bash &&\
    npm install typescript webpack webpack-cli ts-loader &&\
    npm cache clean --force

USER ebook