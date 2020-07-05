FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5567
CMD [ "python3", "./bot.py" ]