# Stressor 

Docker container to stress the CPU

Python flask app which will stress the CPU

It uses Python 3.5 and lookbusy utility to stress the docker container CPU

It useful in doing load testing, autoscaling scenarios where you need to stress container CPU to test CPU based autoscaling rules

You can find more about it at blog https://sbrakl.wordpress.com/2017/01/29/stressor-the-container/

I had develop this app in three flavors

### flaskappwithWerkzeug
Flask stress app running on Werkzeug web server. It good for light weight concurrent loads, but bad for 5+ concurrent load

### flaskappwithSSL
Same as flaskappwithWerkzeug, but configure to run on SSL. It useful in scenarios, where you need to configure containers behind load balancer. This will test load balancer for SSL traffic.

### flaskappwithuwsgi
Flask app is configure to run on the uwsgi and nginx webserver. It configure to run 16 concurrent request. 