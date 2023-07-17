FROM python:3.11-slim-buster
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt update && apt install ssh -y
COPY . /app
ENTRYPOINT ["bash"]
CMD ["run.sh"]
