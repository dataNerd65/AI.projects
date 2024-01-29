# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK data (you can also download NLTK data during runtime if you prefer)
RUN python -m nltk.downloader all

# Run the chatbot script
CMD [ "python", "chatbotMM.py" ]






