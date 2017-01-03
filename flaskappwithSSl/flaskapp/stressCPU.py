import datetime
from math import floor
import flask
import multiprocessing
import subprocess
import time
import psutil
import logging
import socket

def StressCPU(CPU, timeoutinsecs):
    IsCPUValid = IsNumber(CPU) and WithinRange(CPU, 0, 100)
    IsTimeOutValid = IsNumber(timeoutinsecs) and WithinRange(timeoutinsecs, 1, 60)
    hostname = socket.gethostname()
    if (IsCPUValid and IsTimeOutValid):
        flask.session['CPU'] = CPU
        flask.session['timeOutInSecs'] = timeoutinsecs
        flask.session['StartTime'] = datetime.datetime.now()
        fork = multiprocessing.Process(target=fire_lookbusy_cmd, args=(CPU, timeoutinsecs, ))
        fork.start()
        returnobj = GetRunInfo()
    else:
        returnobj = type("returnObj", (object,), dict(HOST=hostname, GivenCPU=CPU, TimeoutInSec=timeoutinsecs,
                                                      PresentCPU="NA", Elapsetime="NA", RemainingTime="NA"))
    return returnobj

def fire_lookbusy_cmd(CPU, timeoutinsecs):
    try:
        intTimeoutinsecs = int(timeoutinsecs)
        numberOfCPU = multiprocessing.cpu_count()
        print("\nStressing CPU to " + CPU + "%")
        p = subprocess.Popen(['lookbusy',
                              '--ncpus', str(numberOfCPU),
                              '--cpu-util', CPU])
        time.sleep(intTimeoutinsecs)
        popAllSessions()
        p.terminate()
    except Exception as e:
        logging.error(e)

def CalculateTime(timeoutinsecs):
    currTime = datetime.datetime.now()
    endTime = currTime + datetime.timedelta(seconds=timeoutinsecs)

def popAllSessions():
    logging.info('Poping all the session out...')
    flask.session.pop('CPU', None)
    flask.session.pop('timeOutInSecs', None)
    flask.session.pop('StartTime', None)
    # flask.session['CPU'] = None
    # flask.session['timeOutInSecs'] = None
    # flask.session['StartTime'] = None

def IsNumber(num):
    try:
        val = int(num)
        return True
    except ValueError:
        return False

def WithinRange(snum, min, max):
    num = int(snum)
    if (num < min and num > max):
        return False
    else:
        return True

def GetRunInfo():
    currTime = datetime.datetime.now()
    hostname = socket.gethostname()
    # Safety check to flush session
    # Hack done, because Session pop does work in different thread in multithreading
    if 'StartTime' in flask.session:
        start_time = flask.session['StartTime']
        session_timeoutInSec = flask.session['timeOutInSecs']
        int_timeout_sec = int(session_timeoutInSec)
        endTime = start_time + datetime.timedelta(seconds=int_timeout_sec)
        if (endTime < currTime):
            popAllSessions()

    #Give CPU
    if 'CPU' in flask.session:
        session_CPU = flask.session['CPU']
    else:
        session_CPU ='NA'

    #Give TimeOut
    if 'timeOutInSecs' in flask.session:
        session_timeoutInSec = flask.session['timeOutInSecs']
    else:
        session_timeoutInSec = 'NA'

    #Current CPU
    presentCPU = psutil.cpu_percent()

    #Elapse Time
    if 'StartTime' in flask.session:
        start_time = flask.session['StartTime']
        elapse_time = currTime - start_time
        elapse_time_formated = format_timedelta(elapse_time, '{hours_total}:{minutes2}:{seconds2}')
    else:
        start_time = None
        elapse_time_formated = 'NA'


    #Remaining Time
    if elapse_time_formated != 'NA':
        int_timeout_sec = int(session_timeoutInSec)
        endTime = start_time + datetime.timedelta(seconds=int_timeout_sec)
        remain_time_formated = date_diff(currTime, endTime)

    else:
        remain_time_formated = 'NA'


    rtnobj = type("returnObj", (object,), dict(HOST=hostname, GivenCPU=session_CPU, TimeoutInSec=session_timeoutInSec,
                                               PresentCPU=presentCPU, Elapsetime=elapse_time_formated,
                                               RemainingTime=remain_time_formated))
    return rtnobj

def date_diff(older, newer):
    """
    Returns a humanized string representing time difference

    The output rounds up to days, hours, minutes, or seconds.
    4 days 5 hours returns '4 days'
    0 days 4 hours 3 minutes returns '4 hours', etc...
    """

    timeDiff = newer - older
    days = timeDiff.days
    hours = timeDiff.seconds/3600
    minutes = timeDiff.seconds%3600/60
    seconds = timeDiff.seconds%3600%60

    str = ""
    tStr = ""
    if days > 1:
        if days == 1:   tStr = "day"
        else:           tStr = "days"
        str = str + "%1.0f %s" %(days, tStr)
        return str
    elif hours > 1:
        if hours == 1:  tStr = "hour"
        else:           tStr = "hours"
        str = str + "%1.0f %s" %(hours, tStr)
        return str
    elif minutes > 1:
        if minutes == 1:tStr = "min"
        else:           tStr = "mins"
        str = str + "%1.0f %s" %(minutes, tStr)
        return str
    elif seconds > 0:
        if seconds == 1:tStr = "sec"
        else:           tStr = "secs"
        str = str + "%1.0f %s" %(seconds, tStr)
        return str
    else:
        return None

def format_timedelta(value, time_format="{days} days, {hours2}:{minutes2}:{seconds2}"):

    if hasattr(value, 'seconds'):
        seconds = value.seconds + value.days * 24 * 3600
    else:
        seconds = int(value)

    seconds_total = seconds

    minutes = int(floor(seconds / 60))
    minutes_total = minutes
    seconds -= minutes * 60

    hours = int(floor(minutes / 60))
    hours_total = hours
    minutes -= hours * 60

    days = int(floor(hours / 24))
    days_total = days
    hours -= days * 24

    years = int(floor(days / 365))
    years_total = years
    days -= years * 365

    return time_format.format(**{
        'seconds': seconds,
        'seconds2': str(seconds).zfill(2),
        'minutes': minutes,
        'minutes2': str(minutes).zfill(2),
        'hours': hours,
        'hours2': str(hours).zfill(2),
        'days': days,
        'years': years,
        'seconds_total': seconds_total,
        'minutes_total': minutes_total,
        'hours_total': hours_total,
        'days_total': days_total,
        'years_total': years_total,
    })