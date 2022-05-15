FROM alpine:3.15

COPY requirements.txt /
RUN apk add --no-cache python3 \
    py3-pip \
    py3-numpy \
    py3-pillow \
    hidapi && \
  pip install -r /requirements.txt
COPY src /app/src

ENTRYPOINT ["python3", "/app/src/main/python/streamdeck/main.py"]
