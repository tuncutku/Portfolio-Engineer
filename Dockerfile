FROM python:3.9.4-slim
COPY . 	/app
WORKDIR /app

RUN ./doit.sh

EXPOSE 5000
CMD ["python3", "run_app.py"]
