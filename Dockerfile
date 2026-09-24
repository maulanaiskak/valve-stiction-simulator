FROM python:3.12-slim

# Unbuffered stdout: without this, print() output sits in Python's block
# buffer (since Docker's stdout isn't a TTY) and never reaches `docker
# logs` until the buffer fills or the process exits.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir paho-mqtt numpy

COPY main.py .
COPY domain/ domain/
COPY delivery/ delivery/

CMD ["python", "main.py"]
