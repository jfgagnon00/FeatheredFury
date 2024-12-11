FROM python:3.12-slim

WORKDIR /app

COPY requirements_app.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/app
# Copier le fichier run_app.py dans l'image
COPY run_app.py /app/run_app.py

EXPOSE 5000

#CMD ["waitress-serve", "--listen", "0.0.0.0:5000", "run_app:app"]
CMD ["waitress-serve", "--port=5000", "run_app:app"]
