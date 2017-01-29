FROM tiangolo/uwsgi-nginx-flask:flask

# Install lookbusy
COPY install-lookbusy.sh /root/
RUN /root/install-lookbusy.sh

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

# copy uwsgi in /etc/uwsgi/uwsgi.ini
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

# copy over our app code
COPY ./flaskapp /app
