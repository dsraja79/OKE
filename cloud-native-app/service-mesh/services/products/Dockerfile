# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the wait-for-it.sh script to the working directory
COPY wait-for-it.sh .

# Update the permissions of the wait-for-it.sh script
RUN chmod +x wait-for-it.sh

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files to the working directory
COPY app.py .
COPY products*.json ./

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app when the container launches
CMD ["python", "app.py"]
