FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

RUN mkdir /app/
WORKDIR /app/
COPY req.txt .

RUN apk add gcc musl-dev zlib-dev jpeg-dev
# these packages are needed for the pillow

RUN pip install -r req.txt

COPY . .
EXPOSE 80
