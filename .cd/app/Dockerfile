ARG PYTHON_VERSION=3.9

FROM python:${PYTHON_VERSION}

WORKDIR /
COPY ../requirements-common.txt .
RUN pip install -r requirements-common.txt && \
    rm requirements-common.txt

CMD ["ffury", "app", "start"]