FROM python:3.11-alpine3.18

WORKDIR /home/milk_app
COPY requirements.txt .
COPY app/ app/
COPY script/entrypoint.sh .

RUN apk add --no-cache bash tzdata && \
  pip install --no-cache-dir -r requirements.txt && \
  rm -rf requirements.txt && \
  chmod +x entrypoint.sh

CMD ["/bin/bash","entrypoint.sh"]
