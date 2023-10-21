FROM python:3.9-slim
LABEL authors="mustafaaktas"

WORKDIR /
COPY data /app/data
COPY database /app/database
COPY src /app/src
COPY app.py /app/app.py

ADD requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "/app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
