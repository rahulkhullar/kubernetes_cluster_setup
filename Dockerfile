# Use an official Python runtime as a parent image
FROM python:3.6.8-stretch

RUN mkdir /etc/restapp
RUN mkdir /opt/restapp
# Set the working directory to /app
WORKDIR /opt/restapp


# Copy the current directory contents into the container at /app
ADD /opt/restapp /opt/restapp
ADD /etc/restapp /etc/restapp

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r /opt/restapp/requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV FLASK_APP /opt/restapp/mysql_api.py

# Run app.py when the container launches
CMD ["/usr/local/bin/gunicorn","--bind", "0.0.0.0:8000", "wsgi"]
#CMD ["python", "mysql_api.py"]
#CMD ["/usr/local/bin/flask","run"]
