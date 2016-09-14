#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session
from onyx.core.models import *
from onyx.core import db
import hashlib


login_manager = LoginManager()
login_manager.init_app(core)

login_manager.login_view = 'hello'



@login_manager.user_loader
def load_user(id):
    return UsersModel.User.query.get(int(id))

@core.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('account/register.html')
    try:
        if request.form['password'] == request.form['verifpassword']:
            hashpass = hashlib.sha1(request.form['password']).hexdigest()
            user = UsersModel.User(username=request.form['username'] , password=hashpass, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash('Compte ajouté avec succés' , 'success')
            return redirect(url_for('hello'))
        else:
            flash('Les mots de passe de sont pas les même !' , 'error')
            return redirect(url_for('register'))
    except:
        flash('une erreur est survenu !' , 'error')
        return redirect(url_for('hello'))

@core.route('/hello')
def hello():
    login_manager.login_view = 'hello'
    return render_template('account/hello.html')
 

@core.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = UsersModel.User.query.filter_by(username=username,password=hashlib.sha1(password).hexdigest()).first()
    if registered_user is None:
        return redirect(url_for('login'))
    login_user(registered_user)
    registered_user.authenticated = True
    flash('Vous vous êtes connecté avec succés', 'success')
    return redirect(request.args.get('next') or url_for('index'))



@core.route('/account/delete' , methods=['GET','POST'])
@login_required
def accountdel():
    if request.method == 'GET':
        try:
            bdd = UsersModel.User.query.all()
            resultUsername = []
            for myusers in bdd:
                resultUsername.append(myusers.username) 
            resultUser = resultUsername

            resultEmailRow = []
            for myusers in bdd:
                resultEmailRow.append(myusers.email) 
            resultEmail = resultEmailRow

            resultIdRow = []
            for myusers in bdd:
                resultIdRow.append(myusers.id) 
            resultId = resultIdRow


            return render_template('account/delete.html' , username=resultUser , email=resultEmail , id=resultId )
        except:
            return render_template('account/delete.html' , error="Pas de comptes")


@core.route('/account/delete/<id_delete>')
def delete_account(id_delete):
    try:
        delete = UsersModel.User.query.filter_by(id=id_delete).first()
        db.session.delete(delete)
        db.session.commit()
        deleteCalendar = CalendarModel.Calendar.query.filter(CalendarModel.Calendar.idAccount.endswith(str(id_delete)))
        db.session.delete(deleteCalendar)
        db.session.commit()
        return redirect(url_for('accountdel'))
    except:
        return redirect(url_for('accountdel', error="Pas de comptes avec cet ID"))


@core.route('/account/manage' , methods=['GET','POST'])
@login_required
def accountManage():
    if request.method == 'GET':
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('account/manage.html' ,buttonColor=buttonColor )
    try:
        user = UsersModel.User.query.filter_by(username=current_user.username).first()
        if hashlib.sha1(request.form['lastpassword']).hexdigest() == user.password:
            if not request.form['color']:
                user.buttonColor = current_user.buttonColor
            else:     
                user.buttonColor = request.form['color']
            if not request.form['username']:
                user.username = current_user.username
            else:
                user.username = request.form['username']
            if not request.form['email']:
                user.email = current_user.email
            else:
                user.email = request.form['email']
            if not request.form['password']:
                user.password = current_user.password
            else:
                user.password = hashlib.sha1(request.form['password']).hexdigest()
            db.session.add(user)
            db.session.commit()
            flash('Compte modifié avec succés' , 'success')
            return redirect(url_for('accountManage'))
        else:
            flash('Les mots de passe de sont pas les même !' , 'error')
            return redirect(url_for('accountManage'))
    except:
        return redirect(url_for('accountManage'))


@core.route('/lock' , methods=['GET','POST'])
def lock():
    if request.method == 'GET':
        login_manager.login_view = 'lock'
        logout_user()
        return render_template('account/lock.html')
    username = current_user.username
    password = request.form['password']
    registered_user = UsersModel.User.query.filter_by(username=username,password=hashlib.sha1(password).hexdigest()).first()
    if registered_user is None:
        return redirect(url_for('lock'))
    login_user(registered_user)
    registered_user.authenticated = True
    return redirect(request.args.get('next') or url_for('index'))

@core.route('/logout' , methods=['GET','POST'])
def logout():
    login_manager.login_view = 'hello'
    logout_user()
    flash('Vous êtes déconnecté' , 'info')
    return redirect(url_for('hello'))