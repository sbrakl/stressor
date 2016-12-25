FROM ubuntu:14.04
MAINTAINER Shabbir Akolawala  "sbrakl@gmail.com"

RUN export TERM=xterm
RUN apt-get update && \
    apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository ppa:fkrull/deadsnakes
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
		    python3.5 \
                    python-pip \
		    python-dev


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
RUN rm -rf lookbusy-1.4*

RUN echo && echo 'Installed lookbusy'
