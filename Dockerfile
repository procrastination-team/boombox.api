FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/start.py"]

EXPOSE 3333