FROM python:3.9.4-slim
LABEL maintainer="tuncutku10@gmail.com"

ENV FLASK_APP=run_app.py
ENV FLASK_CONFIG=docker
ENV SECRET_KEY=${SECRET_KEY}
ENV SECURITY_PASSWORD_SALT=${SECURITY_PASSWORD_SALT}
ENV MAIL_SERVER_EMAIL=portfolioengineerofficial@gmail.com
ENV MAIL_SERVER_PASSWORD=${MAIL_SERVER_PASSWORD}

COPY . 	/app
WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "run_app.py" ]