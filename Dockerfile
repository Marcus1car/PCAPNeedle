FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --nocache-dir -r requirements.txt

COPY src/ /app/
ENTRYPOINT [ "python" , "pcapneedle.py" ]