#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import requests
from onyx.core import core
from onyx.core.assets import getRatpSchedule
from flask import render_template, request , redirect

 
@core.route('/transport')
def transport():
    return render_template('transport/index.html')

@core.route('/transport/rer', methods=['GET', 'POST'])
def rer():
    if request.method == 'POST':
        return redirect('/transport/rer/'+request.form['rerline'])
    return render_template('transport/ratp/rer/index.html')

@core.route('/transport/rer/A', methods=['GET', 'POST'])
def RERA():
    if request.method == 'POST':
        rer = "RA"
        station = request.form['rerstation']
        direction = request.form['rerdirection']
        return render_template('transport/ratp/rer/result.html', result=getRatpSchedule.getRer(rer, station, direction))
    return render_template('transport/ratp/rer/RER A.html')

@core.route('/transport/rer/B', methods=['GET', 'POST'])
def RERB():
    if request.method == 'POST':
        rer = "RB"
        station = request.form['rerstation']
        direction = request.form['rerdirection']
        return render_template('transport/ratp/rer/result.html', result=getRatpSchedule.getRer(rer, station, direction))
    return render_template('transport/ratp/rer/RER B.html')







@core.route('/transport/metro', methods=['GET', 'POST'])
def metro():
    if request.method == 'POST':
        return redirect('/transport/metro/'+request.form['metroline'])
    return render_template('transport/ratp/metro/index.html')

@core.route('/transport/metro/M1', methods=['GET', 'POST'])
def M1():
    if request.method == 'POST':
        line = "1"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        checkbox = request.form.getlist('remember')
        return render_template('transport/ratp/metro/result.html' ,result=getRatpSchedule.getMetro(line, station, direction) , test=checkbox)
    return render_template('transport/ratp/metro/M1.html')

@core.route('/transport/metro/M2', methods=['GET', 'POST'])
def M2():
    if request.method == 'POST':
        line = "2"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M2.html')

@core.route('/transport/metro/M3', methods=['GET', 'POST'])
def M3():
    if request.method == 'POST':
        line = "3"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M3.html')

@core.route('/transport/metro/M3b', methods=['GET', 'POST'])
def M3b():
    if request.method == 'POST':
        line = "3b"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M3b.html')

@core.route('/transport/metro/M4', methods=['GET', 'POST'])
def M4():
    if request.method == 'POST':
        line = "4"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M4.html')

@core.route('/transport/metro/M5', methods=['GET', 'POST'])
def M5():
    if request.method == 'POST':
        line = "5"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M5.html')

@core.route('/transport/metro/M6', methods=['GET', 'POST'])
def M6():
    if request.method == 'POST':
        line = "6"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M6.html')

@core.route('/transport/metro/M7', methods=['GET', 'POST'])
def M7():
    if request.method == 'POST':
        line = "7"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M7.html')

@core.route('/transport/metro/M7b', methods=['GET', 'POST'])
def M7b():
    if request.method == 'POST':
        line = "7b"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M7b.html')

@core.route('/transport/metro/M8', methods=['GET', 'POST'])
def M8():
    if request.method == 'POST':
        line = "8"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M8.html')

@core.route('/transport/metro/M9', methods=['GET', 'POST'])
def M9():
    if request.method == 'POST':
        line = "9"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M9.html')

@core.route('/transport/metro/M10', methods=['GET', 'POST'])
def M10():
    if request.method == 'POST':
        line = "10"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M10.html')

@core.route('/transport/metro/M11', methods=['GET', 'POST'])
def M11():
    if request.method == 'POST':
        line = "11"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M11.html')

@core.route('/transport/metro/M12', methods=['GET', 'POST'])
def M12():
    if request.method == 'POST':
        line = "12"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M12.html')

@core.route('/transport/metro/M13', methods=['GET', 'POST'])
def M13():
    if request.method == 'POST':
        line = "13"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M13.html')

@core.route('/transport/metro/M14', methods=['GET', 'POST'])
def M14():
    if request.method == 'POST':
        line = "14"
        station = request.form['metrostation']
        direction = request.form['metrodirection']
        return render_template('transport/ratp/metro/result.html', result=getRatpSchedule.getMetro(line, station, direction))
    return render_template('transport/ratp/metro/M14.html')

