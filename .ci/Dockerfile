ARG PYTHON_VERSION=3.9-alpine
ARG PORT=80

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY setup.py .
COPY ffury.yaml .
COPY .ci/ .ci/
COPY configs/ configs/
COPY src/ffury/ src/ffury/

RUN pip install --no-cache-dir -r .ci/requirements-app.txt && \
    rm -rf .ci/ && \
    rm setup.py

EXPOSE ${PORT}

# TODO: a refactorer
ENV DOCKER="1"

CMD ["ffury", "app", "--port", ${PORT}]
