# pull official base image
FROM python:3.10.4-alpine

ADD taskhub/requirements.txt /app/requirements.txt

RUN set -ex \
    && apk add --no-cache --virtual .build-deps linux-headers libc-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps


ADD taskhub /app
WORKDIR /app


ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000

# using uwsgi
# CMD ["uwsgi", "--http", ":8000", "--wsgi-file", "taskhub/wsgi.py", "--master", "--processes", "4", "--threads", "2"]

CMD ["python", "manage.py", "runserver"]