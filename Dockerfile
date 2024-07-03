FROM python:3.9.19-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]

EXPOSE 35000