# Use Python slim as the base image
FROM python:slim

# Update pip and install required packages
RUN pip install --upgrade pip && pip install pdm

# Install uvicorn
RUN apt update
RUN apt install -y uvicorn

# Set the working directory to /app
WORKDIR /app

# Copy the bot project files to the container
COPY . .

# Install bot dependencies
RUN pdm sync

# Expose the bot port
EXPOSE 8000

# Start the bot
CMD ["uvicorn", "OptimusMediaServer.app:app", "--reload"]
