FROM python:3.10.6

WORKDIR /

RUN mkdir /src

COPY requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY . /src

EXPOSE 8000

CMD ["gunicorn", "src.core.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]