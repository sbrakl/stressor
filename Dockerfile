FROM ubuntu:14.04
MAINTAINER Shabbir Akolawala  "sbrakl@gmail.com"

RUN apt-get update && \
    apt-get install -y \
                    wget \
                    xz-utils \
                    build-essential \
                    libsqlite3-dev \
                    libreadline-dev \
                    libssl-dev \
                    openssl \
                    nginx \

# Install Python and dev tools like pip and setuptools
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tar.xz
RUN tar -xf Python-3.5.0.tar.xz
WORKDIR /tmp/Python-3.5.0
RUN ./configure
RUN make
RUN make install

# Install Lookbusy
WORKDIR /tmp
RUN wget http://www.devin.com/lookbusy/download/lookbusy-1.4.tar.gz
RUN tar -xzf lookbusy-1.4.tar.gz
WORKDIR /tmp/lookbusy-1.4
RUN ./configure
RUN make
RUN make install
WORKDIR /

# Cleanup
RUN rm -rf /tmp/Python-3.5.0.tar.xz /tmp/Python-3.5.0
RUN rm -rf lookbusy-1.4*

RUN echo && echo 'Install Python 3.5 and lookbusy'

COPY /flaskapp /application
WORKDIR /application
RUN pip install -r requirements.txt