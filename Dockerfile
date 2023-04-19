# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Instale as dependências do sistema operacional para o pacote bson
RUN apt-get update && \
    apt-get install -y libssl-dev libffi-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Run uvicorn server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

