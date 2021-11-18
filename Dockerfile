FROM python:3.7
EXPOSE 5000
WORKDIR /APP
COPY . .
RUN pip install -r requirements.txt
CMD python app.py