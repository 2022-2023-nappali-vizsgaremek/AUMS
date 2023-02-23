FROM python:3.10.7

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "backend/app.py" ]