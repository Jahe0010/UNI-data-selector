FROM python:3.8-buster

WORKDIR /usr/src
#Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#Expose Port and run app
COPY src .
VOLUME ["../logs/", "/logs/"]
CMD ["python", "-u", "main.py"]