FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install python-telegram-bot[job-queue]

COPY *.py ./
COPY moneyspent.sql ./

ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}

CMD ["python", "./main.py"]