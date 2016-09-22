#!/usr/bin/env python
# -*- coding: utf-8 -*-
from onyx.core import core
from flask.ext.login import LoginManager , login_user , login_required , current_user , login_user , logout_user
from flask import request , render_template , redirect , url_for , flash , session
from flask.ext.mail import Message
from onyx.core.models import *
from onyx.core import db , mail
from os.path import exists
import hashlib
import datetime
from itsdangerous import URLSafeTimedSerializer
import os
import onyx

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(core.config['SECRET_KEY'])
    return serializer.dumps(email, salt=core.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(core.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=core.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

login_manager = LoginManager()
login_manager.init_app(core)
login_manager.login_view = 'hello'

def send_mail(recipient , title , message):
    msg = Message(title, sender = 'Onyx', recipients = [recipient])
    msg.html = message
    mail.send(msg)


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
            if exists(str(onyx.__path__[0]) + "/core/config/mail.py") == True:
                user = UsersModel.User(admin=0 ,confirmed_on=datetime.datetime.now(),registered_on=datetime.datetime.now(),confirmed=False, username=request.form['username'] , password=hashpass, email=request.form['email'])
                db.session.add(user)
                db.session.commit()
                token = generate_confirmation_token(request.form['email'])
                confirm_url = url_for('confirm_email', token=token, _external=True)
                html = render_template('account/activate.html', confirm_url=confirm_url)
                subject = "Confirmer votre compte Onyx"
                send_mail(request.form['email'], subject, html)
                login_user(user)
                flash('Un mail de confirmation vient de vous être envoyé.', 'success')
                return redirect(url_for('unconfirmed'))
            else:
                user = UsersModel.User(admin=0 ,confirmed_on=datetime.datetime.now(),registered_on=datetime.datetime.now(),confirmed=True, username=request.form['username'] , password=hashpass, email=request.form['email'])
                db.session.add(user)
                db.session.commit()
                flash('Vous êtes bien inscrit !', 'success')
                return redirect(url_for('hello'))            
        else:
            flash('Les mots de passe de sont pas les même !' , 'error')
            return redirect(url_for('register'))
    except:
        flash('Votre Pseudo ou votre adresse email est déjà prise !' , 'error')
        return redirect(url_for('hello'))

@core.route('/register/resetpassword' , methods=['GET','POST'])
def resetpassword():
    if request.method == 'GET':
        return render_template('account/reset.html' , mail=exists(str(onyx.__path__[0]) + "/core/config/mail.py"))
    try:
        token = generate_confirmation_token(request.form['email'])
        confirm_url = url_for('confirm_reset', token=token, _external=True)
        html = render_template('account/resetMail.html', confirm_url=confirm_url)
        subject = "Changer votre mot de passe Onyx"
        send_mail(request.form['email'], subject, html)
        flash('Un mail vient de vous être envoyé.', 'success')
        return redirect(url_for('resetpassword'))
    except:
        flash("L'adresse mail saisi n'est pas connu de nos services !" , 'error')
        return redirect(url_for('resetpassword'))


@core.route('/register/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('Le lien est invalide ou a expiré.', 'error')
    user = UsersModel.User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Votre compte est déjà confirmé veuillez vous connecter', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Vous avez activé votre compte !', 'success')
    return redirect(url_for('index'))


@core.route('/register/resetpassword/confirm/<token>', methods=['GET','POST'])
def confirm_reset(token):
    if request.method == 'GET':
        try:
            email = confirm_token(token)
        except:
            flash('Le lien est invalide ou a expiré.', 'error')
        user = UsersModel.User.query.filter_by(email=email).first_or_404()
        return render_template('account/resetPassword.html')
    try:
        email = confirm_token(token)
        user = UsersModel.User.query.filter_by(email=email).first()
        user.password = hashlib.sha1(request.form['password']).hexdigest()
        db.session.add(user)
        db.session.commit()
        flash('Mot de passe modifié !' , 'success')
        return redirect(url_for('hello'))
    except:
        flash('Une erreur est survenue !' , 'error')
        return redirect(url_for('hello'))



@core.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('index')
    flash('Veuillez confirmer votre compte !', 'error')
    return render_template('account/unconfirmed.html')

@core.route('/resend')
@login_required
def resend_confirmation():
    if exists(str(onyx.__path__[0]) + "/core/config/mail.py") == True:
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('account/activate.html', confirm_url=confirm_url)
        subject = "Veuillez confirmer votre adresse mail !"
        send_mail(current_user.email, subject, html)
        flash('Un nouveau mail a été envoyé !', 'success')
        return redirect(url_for('unconfirmed'))
    else:
        flash('Vous ne pouvez pas accéder ici !', 'success')
        return redirect(url_for('index'))



@core.route('/hello')
def hello():
    return render_template('account/hello.html')
 

@core.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('account/login.html')
    try:
        email = request.form['email']
        password = request.form['password']
        registered_user = UsersModel.User.query.filter_by(email=email,password=hashlib.sha1(password).hexdigest()).first()
        if registered_user is None:
            flash('Mauvaise adresse email ou mot de passe !', 'error')
            return redirect(url_for('login'))
        if registered_user.confirmed:
            login_user(registered_user)
            registered_user.authenticated = True
            flash('Vous vous êtes connecté avec succés', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            return redirect(url_for('unconfirmed'))
    except:
        flash('Une erreur est survenue !', 'error')
        return redirect(url_for('login'))


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
        for fetch in deleteCalendar:
            deleteEvent = CalendarModel.Calendar.query.filter_by(id=fetch.id).first()
            db.session.delete(deleteEvent)
            db.session.commit()
        deleteTask = TaskModel.Task.query.filter(TaskModel.Task.idAccount.endswith(str(id_delete)))
        for fetch in deleteTask:
            deleteEventTask = TaskModel.Task.query.filter_by(id=fetch.id).first()
            db.session.delete(deleteEventTask)
            db.session.commit()
        flash('Compte supprimé !' , 'success')
        return redirect(url_for('accountdel'))
    except:
        flash('Une erreur est survenue !' , 'error')
        return redirect(url_for('accountdel'))


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

@core.route('/account/manage/color' , methods=['GET','POST'])
@login_required
def changeColor():
    if request.method == 'GET':
        bdd = UsersModel.User.query.filter_by(username=current_user.username).first()
        buttonColor = bdd.buttonColor
        return render_template('account/color.html' ,buttonColor=buttonColor )
    try:
        user = UsersModel.User.query.filter_by(username=current_user.username).first()
        if not request.form['color']:
            user.buttonColor = current_user.buttonColor
        else:
            user.buttonColor = request.form['color']
        db.session.add(user)
        db.session.commit()
        flash('Compte modifié avec succés' , 'success')
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