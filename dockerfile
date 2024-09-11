FROM python:3.12.5-slim

RUN apt-get update
RUN pip install --upgrade pip
RUN apt-get install git -y 
RUN python -m pip install pandas
RUN pip install pygame
RUN pip install pandas
RUN pip install scipy
RUN pip install numpy

WORKDIR /app