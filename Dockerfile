#Use an official python runtime as the base image
FROM python:3.9-slim

#Set the working directory in the container
WORKDIR /ap

# Copy the current directory contents into the container at /app
COPY . /ap

install dependecies
RUN pip install --no-cache-dir numpy spacy scikit-learn

#Download the English model for spaCy
RUN python -m spacy download en_core_web_sm

#Command to run the Python script
CMD ["python", "machinelearningModel.py"]
