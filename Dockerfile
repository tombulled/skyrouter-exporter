FROM python:3.8

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./skyrouter_exporter /code/skyrouter_exporter

RUN pip install .
RUN pip install uvicorn

USER 1001

ENV HOST="192.168.0.1"
ENV USERNAME="admin"
ENV PASSWORD="admin"

CMD ["python", "-m", "uvicorn", "skyrouter_exporter:app", "--host", "0.0.0.0", "--port", "8080"]