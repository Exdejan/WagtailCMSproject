FROM python:3.12-slim-bookworm

RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=CMS.settings.production

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install "gunicorn==20.0.4"

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

COPY --chown=wagtail:wagtail . .

RUN mkdir -p /app/staticfiles && \
    SECRET_KEY=dummy-build-secret \
    DATABASE_URL=sqlite:///dummy.db \
    python manage.py collectstatic --noinput --clear

RUN chown -R wagtail:wagtail /app

USER wagtail

CMD set -xe; python manage.py migrate --noinput; gunicorn CMS.wsgi:application