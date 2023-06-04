ARG BASE_IMAGE=python:3.11.3-slim

FROM ${BASE_IMAGE} as base

WORKDIR /module

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src/ ./src/

EXPOSE 8000
WORKDIR /module/src/
CMD [ "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000" ]