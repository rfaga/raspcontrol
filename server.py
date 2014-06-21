#!/usr/bin/env python

from flask import Flask, render_template, redirect
import subprocess
def run(command):
    try:
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return "Error: command doesn't exist!"
    
    
app = Flask(__name__)

@app.route("/")
def main():
    xbmc = "xbmc start/running" in run("service xbmc status")
    transmission = "daemon is running" in run("service transmission-daemon status")
    return render_template("index.html", xbmc=xbmc, transmission=transmission)

@app.route('/xbmc')
def select_xbmc():
    transmission_stop()
    xbmc_start()
    return redirect('/')

@app.route('/xbmc')
def select_transmission():
    xbmc_stop()
    transmission_start()
    return redirect('/')


@app.route('/xbmcstart')
def xbmc_start():
    run("service xbmc restart")
    run("service xbmc start")
    return redirect('/')

@app.route('/xbmcstop')
def xbmc_stop():
    run("service xbmc stop")
    return redirect('/')

@app.route('/transtop')
def transmission_stop():
    run("service transmission-daemon stop")
    return redirect('/')

@app.route('/transtart')
def transmission_start():
    run("service transmission-daemon start")
    return redirect('/')

@app.route('/reboot')
def system_reboot():
    run("reboot")
    return redirect('/')
    
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=56789)
