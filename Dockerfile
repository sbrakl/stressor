FROM sbrakl/ubuntu-uwsgi-nginx:latest 
MAINTAINER Shabbir Akolawala  "sbrakl@gmail.com"

COPY . /var/stressor
RUN cp /var/stressor/conf/stressor.conf /etc/init/
RUN rm /etc/nginx/sites-enabled/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN cp /var/stressor/conf/nginx.conf /etc/nginx/sites-avaialable/stressor
RUN ln -s /etc/nginx/sites-available/stressor /etc/nginx/sites-enabled
CMD start stressor
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
