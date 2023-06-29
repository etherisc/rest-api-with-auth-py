FROM python

ENV PORT=8000
EXPOSE 8000

# Path: /app
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source code
COPY *py .

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
