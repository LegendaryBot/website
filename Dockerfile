FROM python:3.6.6-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/

EXPOSE 8000

#We install the build dependencies in alpine
RUN set -ex \
    && apk add --no-cache --virtual .build-deps  \
		bzip2-dev \
		coreutils \
		dpkg-dev dpkg \
		expat-dev \
		gcc \
		gdbm-dev \
		libc-dev \
		libffi-dev \
		linux-headers \
		make \
		ncurses-dev \
		libressl \
		libressl-dev \
		pax-utils \
		readline-dev \
		sqlite-dev \
		tcl-dev \
		tk \
		tk-dev \
		xz-dev \
        zlib-dev \
        postgresql-dev \
        git \
        && apk add postgresql \
        && pip install -r requirements.txt \
        && pip install -U git+https://github.com/python-social-auth/social-core.git \
        && apk del .build-deps
RUN python manage.py migrate
RUN python manage.py collectstatic
CMD ["gunicorn", "legendarybot.wsgi:application", "--workers 3", "-b 0.0.0.0:8000"]