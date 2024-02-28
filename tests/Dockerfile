FROM python:3.9-slim

WORKDIR /opt/one-time-secret
COPY tests/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

ENTRYPOINT ["pytest", "-s"]
