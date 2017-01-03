from flask import Flask, render_template, request, session
import socket
import stressCPU
import os
import logging

logging.basicConfig(level=logging.INFO)


application = Flask(__name__)
application.secret_key = os.urandom(24)

@application.route('/test')
def hello_world():
    return 'Hello, World!'

@application.route('/')
def display_page():
    hostname = socket.gethostname()    
    ip = socket.gethostbyname(hostname)
    return render_template("index.html", IP=ip, HOST=hostname)

@application.route('/stress', methods = ['POST'])
def display_stress_page():
    req_CPU = request.form['CPU']
    req_timeoutInSec = request.form['timeoutInS']
    rtnobj = stressCPU.StressCPU(req_CPU, req_timeoutInSec)
    return  render_template("stress.html", Resp = rtnobj)

@application.route('/refresh', methods = ['GET'])
def display_refresh_page():
    rtnobj = stressCPU.GetRunInfo()
    return  render_template("stress.html", Resp = rtnobj)


if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', use_reloader=False)