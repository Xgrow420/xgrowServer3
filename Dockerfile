
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./XgrowServer /code/XgrowServer

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "XgrowServer.main:app" , "--host", "0.0.0.0", "--port", "80", "--workers" , "1"]

#https://fastapi.tiangolo.com/deployment/docker/


#FROM python:3.9
#
#WORKDIR /code
#
#COPY ./requirements.txt /code/requirements.txt
#
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
#COPY ./app /code/app
#
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
##CMD ["uvicorn", "XgrowServer.main:app", "--host", "0.0.0.0", "--port", "80"]



#FROM python:3.8-slim-buster
#
#WORKDIR /app
#
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#
#COPY . .
#
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]