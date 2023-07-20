FROM python:3.10.6

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV DB_HOST=shapetracker-mysql
ENV DB_NAME=shapeTracker
ENV DB_USER=flask
ENV DB_PASSWORD=flask

EXPOSE 5000

CMD ["python","app.py"]


