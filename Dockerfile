# Use an official Python runtime as a parent image
FROM python:3.6.8-stretch

RUN mkdir /etc/restapp
RUN mkdir /opt/restapp
# Set the working directory to /app
WORKDIR /etc/restapp


# Copy the current directory contents into the container at /app
ADD /restapi /etc/restapp
ADD config.ini /opt/restapp

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /etc/restapp/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "mysql_api.py"]
