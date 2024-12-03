FROM python:3.9-slim

WORKDIR /api  
 
COPY requirements_api.txt /api/requirements.txt 
 
RUN pip install --no-cache-dir -r requirements.txt
  
COPY /api /api/api
 
COPY run_api.py /api/run_api.py

EXPOSE 8080

#CMD ["python3", "run_api.py"]
#CMD ["waitress-serve", "--listen", "0.0.0.0:8080", "run_api:api"]
CMD ["waitress-serve", "--port=8080", "run_api:api"]