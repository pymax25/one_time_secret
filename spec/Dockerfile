FROM python:3.9-slim

WORKDIR /opt/one-time-secret

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

ENTRYPOINT ["python", "-u"]
CMD ["main.py"]
