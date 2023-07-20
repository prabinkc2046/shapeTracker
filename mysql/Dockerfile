FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=prabin123
ENV MYSQL_USER=flask
ENV MYSQL_PASSWORD=flask
ENV MYSQL_DATABASE=shapeTracker

COPY create_table.sql /docker-entrypoint-initdb.d/create_table.sql

