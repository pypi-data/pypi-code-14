#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from onyx.core.assets import getMusic
from flask import render_template , redirect , url_for, request ,flash
from flask import send_file
from werkzeug import secure_filename
from flask.ext.login import login_required
import os


@core.route('/music', methods = ['GET', 'POST'])
@login_required
def music():
    if request.method == 'GET':
        music = os.listdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/music')
        return render_template('music/index.html' , music=music)
    f = request.files['musicfile']
    if f:
        nom = secure_filename(f.filename)
        f.save(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/music/' + nom)
        flash('La musique a bien été enregistrée' , 'success')
        return redirect(url_for('music'))

@core.route('/music/play')
@login_required
def play():
    getMusic.launch()
    getMusic.play()
    return redirect(url_for('music'))

@core.route('/music/pause')
@login_required
def pause():
    getMusic.pause()
    return redirect(url_for('music'))

@core.route('/music/stop')
@login_required
def stop():
    getMusic.stop()
    return redirect(url_for('music'))


@core.route('/music/next')
@login_required
def next():
    getMusic.next()
    return redirect(url_for('music'))


@core.route('/music/previous')
@login_required
def previous():
    getMusic.previous()
    return redirect(url_for('music'))


@core.route('/music/<music_delete>')
def delete_music(music_delete):
    try:
        os.remove(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + '/static/music/' + music_delete))
        return redirect(url_for('music'))
    except:
        return redirect(url_for('music', error="Pas de Musique avec cet ID"))
