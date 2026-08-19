FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_ROOT_USER_ACTION=ignore
WORKDIR /srv

COPY be/requirements.txt ./be-requirements.txt
COPY tests/requirements.txt ./test-requirements.txt
RUN pip install --no-cache-dir -r be-requirements.txt -r test-requirements.txt

COPY shared ./shared
RUN pip install --no-cache-dir ./shared
COPY be ./be
COPY tests ./tests

WORKDIR /srv/tests
CMD ["pytest"]
