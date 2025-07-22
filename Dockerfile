FROM python:3.9-slim

ENV PYTHONPATH="/app/:${PYTHONPATH}"
ENV GROUP_ID=1000 \
    USER_ID=1000

RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5057

#CMD ["gunicorn", "main:app", "-w", "4", "--bind", "0.0.0.0:5057"]
CMD ["python", "main.py"]
