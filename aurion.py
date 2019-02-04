#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 22:43:22 2018

@author: clement
"""
#Affichage du programme
"""------------------AURION CALENDAR------------------
   |       parce qu'il est trop chiant de base...     |
   |               par Clément SANCHEZ                |
   |                    V2.0.12                       |
   ---------------------------------------------------"""

import os
from selenium import webdriver
from ics import Calendar, Event
from uuid import uuid4
import time
import version as V
from pyvirtualdisplay import Display

#merci à BDeliers pour le formatage des données plus simple clair que ce que j'avais fait : https://github.com/BDeliers/Python-Planning-Aurion/blob/master/aurion.py
from datetime import datetime, timedelta
from time import mktime, sleep
from xml.etree import ElementTree as etree
import json

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

#define la version de mon fetcher
class Aurion():
    vers = V.version

    #display = Display(visible=0,size=(1024,768))
    #display.start()
    
    def __init__(self,passwE,userE,dateUser):
        self.passw = passwE
        self.user = userE
        self.c = Calendar()
        self.emploie = []
        self.idenC = uuid4()
        self.dateS = datetime.now() - timedelta(hours = datetime.now().hour) - timedelta(minutes = datetime.now().minute) - timedelta(days=1)*datetime.now().weekday()
        if dateUser == 'Nweek':
            self.dateS = self.dateS + timedelta(days=7)
            print('Nweeeeeek')
        
        if dateUser == 'month':
            self.dateF = '1546725600000'
        else:
            self.dateF = self.dateS + timedelta(days=6)
        self.dateS = str(int(mktime(self.dateS.timetuple())) *1000)
        if dateUser != 'month':
            self.dateF = str(int(mktime(self.dateF.timetuple())) *1000)
        else:
            self.dateF = str(self.dateF)
        print("DateStart : {}, dateFin : {}".format(self.dateS,self.dateF))
    def _info(self):
        return self.info
    
    def iden(self):
        return self.idenC
    
    def connexion(self):
               
        #chrome option
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        #driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
        self.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
                
        # Open the website
        self.driver.get('https://aurion-lille.yncrea.fr/faces/Login.xhtml')
        
        # Select the id box
        logbox = self.driver.find_element_by_id('username')
        passbox = self.driver.find_element_by_id('password')
        
        # Send id information
        logbox.send_keys(self.user)
        passbox.send_keys(self.passw)
        # Find login button
        login_button = self.driver.find_element_by_id('j_idt27')
        #login_button = self.driver.find_element_by_link_text('Connexion')
        # Click login
        try:
            login_button.click()
            try:
                alert = driver.switch_to.alert
                pass
            except:
                if 'erreur' in self.driver.current_url:
                    self.info= "NotCoPass"
                    self.driver.close()
                else:
                    self.info= "Connected"
                pass
            pass
        except :
            self.info= "NotCoNull"
            self.driver.close()
            pass
        print self.info
        return self.info


    def planning(self):
        #with open('var/www/aurion.com/aurionapp/static/test'+ str(self.id) + '.txt', 'w') as f:
        #with open('static/ISEN_emploi'+ str(uid) + '.ics', 'w') as f:
        #    f.writelines(self.id)
        #    f.close()
        a = self.driver.find_element_by_link_text('Mon Planning')
        self.info= "Ouverture du planning"
        self.driver.execute_script("arguments[0].click();", a)
        if 'Planning' in self.driver.current_url:
            print("Récupération du planning")
            print("    ViewState récupération")
            viewS = self.driver.find_element_by_id('j_id1:javax.faces.ViewState:0')
            viewState = viewS.get_attribute('value')
            print('    ViewState : ' + viewState)
            form = self.driver.find_element_by_class_name("schedule").get_attribute("id")
            post = 'xhttp.send("javax.faces.partial.ajax=true&javax.faces.source='+form+'&javax.faces.partial.execute='+form+'&javax.faces.partial.render='+form+'&'+form+'='+form+'&'+form+'_start='+self.dateS+'&'+form+'_end='+self.dateF+'&form=form&form%3AlargeurDivCenter=1606&'+form+'_view=agendaWeek&form%3AoffsetFuseauNavigateur=-7200000&form%3Aonglets_activeIndex=0&form%3Aonglets_scrollState=0&javax.faces.ViewState=' + viewState + '");'
            print("    Exécution du script")
            self.driver.execute_script("""var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                document.getElementById('j_idt18').innerText = this.responseText;
                }
                else{return false;}
                };
                xhttp.open("POST", "/faces/Planning.xhtml", true);
                xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded"); """ + post)
            self.info= "    Attente du résultat"
            data = self.driver.execute_script('return document.getElementById("j_idt18").innerText ;')
            while data=='':
                time.sleep(0.5)
                data = self.driver.execute_script('return document.getElementById("j_idt18").innerText ;')
            #data = data[data.find('j_idt'+form) + 32:data.find('id="form:j_idt135') - 17]
            #data.encode('UTF-8')
            self.emploie = formateData(data,int(self.dateS))
            self.info= "Fini"
        else:
            print("ERROR")
        self.driver.close()
        return self.info
        
        
    def creationCaledrier(self):
        def createICS(typ,deb,fin,matiere,salle,prof):
            e = Event()
            e.name = "{} - {}".format(salle,matiere)
            e.begin = deb
            e.end = fin
            e.location = salle
            e.description = "{}: {} en {} par {}".format(typ,matiere,salle,prof)
            self.c.events.add(e)
        
        for ev in self.emploie:
            #print ev
            #createICS(typ,deb,fin,matiere,salle):
            createICS(ev['type'],ev['debut'],ev['fin'],ev['cours'],ev['salle'],ev['prof'])
        uid = uuid4()
        
        #with open('var/www/aurion.com/aurionapp/static/ISEN_emploi'+ str(uid) + '.ics', 'w') as f:
        with open('static/ISEN_emploi'+ str(uid) + '.ics', 'w') as f:
            f.writelines(self.c)
            f.close()
        return str(uid)


def formateData(data,Stime):
    # Retour en XML
    xml = etree.fromstring(data)
    # On parse la parti intéressante en JSON
    events = json.loads(xml.findall(".//update")[1].text)["events"]

    eventsFormatted = []
    idEvent = []
    # On formatte un peu tout ça
    for i in range(0, len(events)):
        tmp = events[i]["title"]
        tmp = tmp.split("-")
        for j in range(0, len(tmp)):
            # Espaces en début/fin
            tmp[j] = tmp[j].strip()
        # Les noms de profs
        # Remplacer les slashes par des virgules
        tmp[4] = tmp[4].replace('/', ',')
        # En minuscule
        tmp[4] = tmp[4].lower()
        # Première lettre en majuscule
        tmp[4] = tmp[4].title()
        idEv = events[i]["id"]
        ContinueEv = True
        for ide in idEvent:
            if idEv == ide:
                ContinueEv = False
                break
        timeEv = events[i]["start"]
        timeEv = int(mktime(datetime.strptime(timeEv[:-5], "%Y-%m-%dT%H:%M:%S").timetuple())) *1000
        #print("Ev: {}, Stime: {}".format(timeEv,Stime))
        if timeEv > Stime:
            if ContinueEv != False:
                idEvent.append(idEv)
                # Un bel évèneent formatté
                tmp = {"id":events[i]["id"],"debut":events[i]["start"], "fin":events[i]["end"], "type":tmp[3], "cours":tmp[4], "prof":tmp[5], "salle":tmp[0], "titre":tmp[4]}
                # On l'ajoute à la liste
                eventsFormatted.append(tmp)
    
    return eventsFormatted