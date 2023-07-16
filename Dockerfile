FROM python:3.9-slim
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python", "main.py" ]
