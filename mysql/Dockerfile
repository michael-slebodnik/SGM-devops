FROM mysql

ENV MYSQL_ROOT_PASSWORD:=password
ENV MYSQL_DATABASE=weather

COPY init.sql /docker-entrypoint-initdb.d
