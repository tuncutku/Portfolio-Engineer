FROM python:3.7-slim
COPY . 	/app
WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/docker.txt

EXPOSE 5000
CMD ["python3", "run.py"]
