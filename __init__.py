from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_mysqldb import MySQL, MySQLdb

from flask_mail import Mail , Message

from datetime import datetime

#pour le fichier
import xlrd
import MySQLdb

# from flask_login import LoginManager, UserMixin
# import flask_login
# import bcrypt
# import hashlib


app = Flask(__name__)
# login = LoginManager(app)
# # app.secret_key = 'many random bytes'

# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Trucs mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'passer'
app.config['MYSQL_DB'] = 'simed'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




mail = Mail()
mail.init_app(app)

mysql = MySQL(app)




# Page des dossiers médicaux
@app.route('/page_medecin/dossiers_medicaux')
def lister_dossiers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT prenom, nom, date_naissance, telephone, adresse FROM dossier_medical")
    rows = cur.fetchall()
    cur.close()
    return render_template('pages_admin/index.html', dossiers = rows)


# Page des consultations
@app.route('/page_medecin/consultations')
def lister_consultations():
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, motif, medecin.prenom, medecin.nom FROM consultation,medecin where consultation.medecin=medecin.id")
    rows = cur.fetchall()
    cur.close()
    return render_template('pages_admin/consultations.html', consultations = rows)
    

# Page de l'ordonnance choisie
@app.route('/page_medecin/ordonnance')
def lister_ordonnance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT medicaments.nom, quantite, administration, type, renouvellement, posologie FROM ordo_medicament,medicaments where ordo_medicament.medicament=medicaments.id and ordo_medicament.ordonnance=ordonnance.id")
    rows = cur.fetchall()
    cur.close()
    return render_template('pages_admin/ordonnance.html', ordonnances = rows)


# Page des examens et vaccins
@app.route('/page_medecin/examens')
def lister_examens():
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, examen.nom FROM examen,examens where examen.id=examens.examen")
    rows = cur.fetchall()
    cur.close()
    curs = mysql.connection.cursor()
    curs.execute("SELECT date, vaccins.vaccin, vaccinateur FROM vaccin_consultation, vaccins WHERE vaccin_consultation.vaccin=vaccins.id")
    row = curs.fetchall()
    curs.close()
    return render_template('pages_admin/examens.html', examens = rows, vaccins = row )


# Page des antecedents et allergies
@app.route('/page_medecin/antecedents')
def lister_antecedents():
    cur = mysql.connection.cursor()
    cur.execute("SELECT libelle, type FROM antecedents, dossier_medical where antecedents.dossier=dossier_medical.id")
    rows = cur.fetchall()
    cur.close()
    curs = mysql.connection.cursor()
    curs.execute("SELECT nom, consultation.date FROM allergies, consultation where allergies.consultation=consultation.id")
    row = curs.fetchall()
    curs.close()
    return render_template('pages_admin/antecedents.html', antecedents = rows, allergies = row)



# Page des rendez-vous et hospitalisations
@app.route('/page_medecin/hostpitalisations')
def lister_hospitalisations():  
    cur = mysql.connection.cursor()
    cur.execute("SELECT rv.date, heure, hopital, docteur from rv ")
    rows = cur.fetchall()
    cur.close()
    curs = mysql.connection.cursor()
    curs.execute("SELECT date_entree, date_sortie, motif, hopital.nom, medecin.nom FROM hospitalisation, hopital, medecin where hospitalisation.hopital=hopital.id and hospitalisation.medecin=medecin.id")
    row = curs.fetchall()
    return render_template('pages_admin/hospitalisations.html', hospitalisations = row, rvs = rows)






if __name__ == '__main__':
    app.run(debug = True, port = 5000)