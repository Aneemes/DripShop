# Use the official Python image as the base image
FROM python:3.11.4

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=dripshop.settings.dev"]