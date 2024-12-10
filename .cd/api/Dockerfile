ARG PYTHON_VERSION=3.12-slim
ARG PORT=8080

FROM python:${PYTHON_VERSION}

# TODO: ajouter un user non root
WORKDIR /api

COPY setup.py .
COPY ffury.yaml .
COPY .ci/ .ci/
COPY configs/ configs/
COPY src/ffury/ src/ffury/

RUN pip install --no-cache-dir -r .ci/requirements-web.txt && \
    rm -rf .ci/ && \
    rm setup.py

# TODO: a refactorer
ENV DOCKER="1"

EXPOSE ${PORT}

# TODO: revoir le demarrage
# CMD ["ffury", "api", "--port", ${PORT}]
# CMD ["waitress-serve", "--port=8080", "run_api:api"]
CMD ["bash"]
