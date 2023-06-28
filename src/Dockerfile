FROM python:3.10.6

RUN mkdir /project

WORKDIR /project

RUN mkdir /project/src

COPY requirements.txt /project/src/requirements.txt

RUN pip install -r /project/src/requirements.txt

COPY . /project/src

EXPOSE 8000

CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]