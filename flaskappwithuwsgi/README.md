### flaskappwithuwsgi
Flask app is configure to run on the uwsgi and nginx webserver. It configure to run 16 concurrent request. 

Command to run docker container would be 

docker run -p 80:5000 --name stressor sbrakl\stressor:uwsgi