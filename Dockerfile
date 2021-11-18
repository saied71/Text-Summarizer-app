FROM python:3.7
EXPOSE 5000
WORKDIR /APP
COPY . .
CMD sudo apt-get install python3-dev
RUN pip install -r requirements.txt
CMD python app.py