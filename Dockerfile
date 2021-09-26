FROM python:3.8

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY . /src

EXPOSE 80

CMD ["uvicorn", "model:app", "--host", "0.0.0.0", "--port", "80"]
