#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:05:41 2018

@author: clement
"""

from flask import Flask,render_template,redirect,url_for,request,jsonify,send_file,session
from flask_mail import Mail, Message

import datetime

import aurion
import version as V
import os

app = Flask(__name__)
app.secret_key = 'secretKey'
#permet de configurer la vie de la session de 15 jours
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=15)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aurion.calendar@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('G_AURION')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

Client = {}
@app.route('/login/')
@app.route('/')
def index():
    return render_template('index.html',version=V.version)  

@app.route('/error/')
def envoye_erreur():
    return render_template('retour.html',version=V.version)
@app.route('/send_error/', methods=['POST','GET'])
def send_error():
    if request.method == 'POST':
        email_U = request.form.get('email')
        message_U = request.form.get('message')
        print 'email :{},text:{}'.format(email_U,message_U)
        if email_U != '' and  message_U != '':
            msg = Message('Error dans Aurion Calendar', sender = email_U, recipients = ['clement.sanchez@isen.yncrea.fr'])
            msg.body = "{} a trouver une erreur : \n{}".format(email_U,message_U)
            mail.send(msg)
            return 'OK',200
        else:
            return 'err',417
    return redirect(url_for('envoye_erreur'))

#Lance la récupération du calendrier
@app.route('/connexion/', methods=['POST','GET'])
def start_calendrier():
    if request.method == 'POST':
        passw = request.form['pass']
        #user = request.args.get('user')
        user = request.form['user']
        dateUser = request.form['date']
        #print dateUser
        print('pass:' + passw +'\nuser :' + user)
        if passw is None or user is None :
            return jsonify({'status':'NotCoNull'}),418
        else:
            #calen = aurion.Aurion(passw,user,dateUser)
            calen = aurion.Aurion(passw,user,dateUser)
            co = calen.connexion()
            if co == 'Connected':
                iden = calen.iden()
                session['calendrier'] = iden
                Client[iden] = calen
                statusCalen = [{'loader':'hide','valid':'','status':'Connecté'},{'loader':'','valid':'hide','status':'Récupération des données'}]
                return jsonify({'data': render_template("info.html",posts = statusCalen),'status':'ok'})
            else:
                return jsonify({'status':co}),418
    else:
        return redirect(url_for('index'))

@app.route('/planning/',methods=['POST'])
def recup_planning():
    calenID = session['calendrier']
    calen = Client[calenID]
    calen.planning()
    statusCalen = [{'loader':'hide','valid':'','status':'Connecté'},{'loader':'hide','valid':'','status':'Récupération des données'},{'loader':'','valid':'hide','status':'Création du calendrier'}]
    return jsonify({'data': render_template("info.html",posts = statusCalen),'status':'ok'})

@app.route('/create_calen/',methods=['POST'])
def create_calen():
    calenID = session['calendrier']
    calen = Client[calenID]
    uuid = calen.creationCaledrier()
    Client.pop(calenID,None)
    session.pop('calendrier',None)
    return jsonify({'data': render_template("download.html",title="Vous pouvez télécharger votre fichier",role='success',uid = uuid),'status':'ok'})

#@app.route('/client/',methods=['GET'])
#def client():
#    print Client
#    return 'Le nombre de connexion est : {}'.format(len(Client))

#permet de dl le calendrier
@app.route('/return_ics/<id>')
def return_file(id=None):
    if id is None:
        return None
    else:
        return send_file('static/ISEN_emploi'+ id+'.ics', attachment_filename='ISEN_emploi.ics')


@app.errorhandler(401)
@app.errorhandler(404)
def ma_page_erreur(error):
    return "Vous êtes sur une page d'erreur "

if __name__ == "__main__":
    app.run(debug=True)