FROM python:slim
RUN pip install --upgrade pip && pip install pdm
RUN apt update
RUN apt install -y uvicorn
WORKDIR /app
COPY . .
RUN pdm sync
EXPOSE 8000
CMD ["pdm", "run", "uvicorn", "OptimusMediaServer.app:app", "--reload", "--host", "0.0.0.0"]
