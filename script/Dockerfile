FROM python:3.11-slim

WORKDIR /home/milk_app
COPY requirements.txt .
COPY app/ app/
COPY script/entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt && \
  rm -rf requirements.txt && \
  chmod +x entrypoint.sh

CMD ["/bin/bash","entrypoint.sh"]
