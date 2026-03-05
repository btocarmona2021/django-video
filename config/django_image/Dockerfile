FROM python:3.12

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gcc

WORKDIR /usr/src/app

RUN pip install --upgrade pip setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

