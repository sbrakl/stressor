FROM python:3.5
MAINTAINER Shabbir Akolawala  "sbrakl@gmail.com"

# Install lookbusy
COPY install-lookbusy.sh /root/
RUN /root/install-lookbusy.sh

# Copy StartupScript
COPY ./startupscript /var/runscripts/

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy over our app code
RUN mkdir /app
COPY ./flaskapp /app

# setup application certificate and run app
ENV FLASK_APP main.py
CMD ["bash", "/var/runscripts/run.sh", "-x"]
