from flask import Flask, render_template, request, session
import socket
import stressCPU
import os
import logging
import ssl

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/test')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def display_page():
    hostname = socket.gethostname()    
    ip = socket.gethostbyname(hostname)
    return render_template("index.html", IP=ip, HOST=hostname)

@app.route('/stress', methods = ['POST'])
def display_stress_page():
    req_CPU = request.form['CPU']
    req_timeoutInSec = request.form['timeoutInS']
    rtnobj = stressCPU.StressCPU(req_CPU, req_timeoutInSec)
    return  render_template("stress.html", Resp = rtnobj)

@app.route('/refresh', methods = ['GET'])
def display_refresh_page():
    rtnobj = stressCPU.GetRunInfo()
    return  render_template("stress.html", Resp = rtnobj)


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('server.crt', 'server.key')
    app.run(debug=True, host='0.0.0.0', ssl_context=context, threaded=True, use_reloader=False)
