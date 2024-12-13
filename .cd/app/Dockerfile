# ARG PYTHON_VERSION=3.12-slim
# ARG PORT=5000

# FROM python:${PYTHON_VERSION}

# # TODO: ajouter un user non root
# WORKDIR /app

# COPY setup.py .
# COPY ffury.yaml .
# COPY .ci/ .ci/
# COPY configs/ configs/
# COPY src/ffury/ src/ffury/

# RUN pip install --no-cache-dir -r .ci/requirements-web.txt && \
#     rm -rf .ci/ && \
#     rm setup.py

# # TODO: a refactorer
# ENV DOCKER="1"

# EXPOSE ${PORT}

# # TODO: revoir le demarrage
# # CMD ["ffury", "app", "--port", ${PORT}]
# CMD ["bash"]
ARG PYTHON_VERSION=3.9
ARG PORT=5000

FROM python:${PYTHON_VERSION}

WORKDIR /app

COPY app.py .

RUN pip install --no-cache-dir flask==3.1.0

EXPOSE ${PORT}

CMD ["python", "app.py"]
