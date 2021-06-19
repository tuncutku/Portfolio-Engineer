FROM python:3.9.4-slim
LABEL maintainer="tuncutku10@gmail.com"

COPY . 	/app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["run_app.py"]
