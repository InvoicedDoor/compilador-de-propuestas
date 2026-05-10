FROM python:3.12 AS development

WORKDIR /app

COPY requirements-linux.txt .

RUN pip3 install -r requirements-linux.txt

COPY . .

CMD ["python3", "app.py"]