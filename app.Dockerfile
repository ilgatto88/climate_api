FROM python:3.10.6
RUN mkdir /app
WORKDIR /app
RUN cd /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.core:app", " - host", "127.0.0.1", " - port", "8000", " - log-level", "debug"]