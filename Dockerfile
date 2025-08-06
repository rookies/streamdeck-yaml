FROM alpine:3.22.1

COPY requirements.txt /
RUN apk add --no-cache python3 \
    py3-pip \
    py3-numpy \
    py3-pillow \
    hidapi && \
  python -m venv --system-site-packages /venv && \
  PATH=/venv/bin:$PATH pip install -r /requirements.txt
COPY src /app/src

ENV PATH="/venv/bin:$PATH"
ENTRYPOINT ["python", "/app/src/main/python/streamdeck/main.py"]
