### flaskappwithuwsgi
Flask app is configure to run on the uwsgi and nginx webserver. It configure to run 16 concurrent request. It based on tiangolo/uwsgi-nginx-flask:flask docker container

Command to run docker container would be 

docker run -p 80:5000 --name stressor sbrakl\stressor:uwsgi

Here are the description of the files

#### uwsgi.ini
It is configuration file which configure uwsgi. It controls number of treads, and various other uwsgi parameters.

#### requirements.txt
List of pip packages need to install to run the app. Flask isn't there, as it come with based docker container, tiangolo/uwsgi-nginx-flask:flask

#### install-lookbusy.sh
Bash script to install lookbusy