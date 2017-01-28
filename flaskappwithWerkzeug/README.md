### flaskappwithWerkzeug
Flask stress app running on Werkzeug web server. It good for light weight concurrent loads, but bad for 5+ concurrent load

Command to run docker container would be 

docker run -p 80:5000 --name stressor sbrakl\stressor:latest