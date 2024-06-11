FROM python:3.12-slim

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY  *.py ./
COPY .env ./
COPY *.txt ./

EXPOSE 514

CMD [ "python", "./GlobalProtect_IP-Blocker.py" ]