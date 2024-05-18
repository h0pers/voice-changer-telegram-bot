FROM python:3.11.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
RUN python -m pip install --upgrade pip && pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
