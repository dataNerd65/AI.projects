# Use an appropriate base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY machinelearningModel.py .

# Copy the data files into the container
COPY questions+categories.txt .
COPY responses.txt .

# Install spaCy and download the English model
RUN pip install spacy && \
    python -m spacy download en_core_web_sm

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Define the command to run your Python script
CMD ["python", "machinelearningModel.py"]




