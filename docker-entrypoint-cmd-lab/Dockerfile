#FROM python:3.12-alpine

#WORKDIR /app

#COPY calculator.py .

#ENTRYPOINT ["python", "calculator.py"]

#CMD ["10", "5"]

#*****FoR entrypoint.sh******#
FROM python:3.12-alpine

WORKDIR /app

COPY calculator.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "calculator.py", "10", "5"]
