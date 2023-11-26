# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:12:01 2023

@author: user
"""

import json
from flask import Flask, render_template, request, redirect, url_for,session, jsonify, send_file
from equipment_manager import EquipmentManager
from werkzeug.security import check_password_hash, generate_password_hash
import logging, subprocess
import schedule
import time

logging.basicConfig( level=logging.DEBUG, filename='app.log')

logger = logging.getLogger('Journal_exemple')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug('Information-Debug')
logger.info('Message info')
logger.warning('avertissement')
logger.critical('erreur grave')
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)


logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Flask(__name__)
manager = EquipmentManager('equip.json')
manager_data = EquipmentManager('equip_data_oid.json')
users_data = {}
# Configurez le système de journalisation

# Variable booléenne initiale
etat_SNMP = False

def load_users_data():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Fonction pour récupérer les données des agents SNMP
@app.route('/collect_snmp_data')
def collect_snmp_data():
    manager.collect_snmp_data()
    equipment_list = manager.get_equipment_list()

    if etat_SNMP==True:
        print("Collecting SNMP data...")

        for equipment in equipment_list:
            nom = equipment['Nom']
            adresse_ip = equipment['AdresseIP']
            if equipment['SNMP'] == 'v3':
                username = equipment['Username']
                auth_protocol = equipment['AuthProtocol']
                auth_password = equipment['AuthPassword']
                privacy_protocol = equipment['PrivacyProtocol']
                privacy_password = equipment['PrivacyPassword']

                commande = './multi_SNMP_v3.sh ' + adresse_ip + ' ' + username + ' ' + auth_protocol + ' ' + auth_password + ' ' + privacy_protocol + ' ' + privacy_password
                process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)
                sortie = process.stdout.read().decode()
            else:
                communaute = equipment['community']

                commande = './multi_SNMP_v2c.sh ' + communaute + ' ' + adresse_ip
                process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)
                sortie = process.stdout.read().decode()

            if sortie.strip():
                print(f"Finish collecting SNMP data for {adresse_ip}")
                OID = sortie.split('\n')
                for i, ligne in enumerate(OID):
                    OID[i] = ligne[:-1]

                manager_data.add_data_equip(nom, adresse_ip, OID)


# Planifiez la fonction pour s'exécuter toutes les 5 minutes (modifiable selon vos besoins)
schedule.every(1).minutes.do(collect_snmp_data)

# Fonction pour exécuter la planification en arrière-plan
def job():
    while True:
        schedule.run_pending()
        time.sleep(1)


@app.route('/')
def index():
    msg_add_equipement = session.pop('msgAddEquipement', '')  # Récupérez le message de la session

    if not session.get('logged_in'):
        return redirect(url_for('login'))
    equipment_list = manager.get_equipment_list()
    return render_template('index.html', equipment_list=equipment_list, msgAddEquipement=msg_add_equipement, etatSNMP=etat_SNMP)

@app.route('/toggle', methods=['POST'])
def toggle():
    global etat_SNMP
    data = request.get_json()
    new_state = data['newState']
    etat_SNMP = new_state
    if etat_SNMP == True:
        logging.info("INFO: Controlleur Lancer")
    else:
        logging.info("INFO: Controlleur Desactiver")
    return jsonify({"success": True})

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    nom = request.form['nom']
    adresse_ip = request.form['adresse_ip']
    port = request.form['port']
    communaute = request.form['communaute']

    #----------execution du code pour vérification--------------------------
    if etat_SNMP==True:
        commande = './multi_SNMP_v2c.sh ' + communaute + ' ' + adresse_ip
        process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)
        sortie = process.stdout.read().decode()

        if sortie.strip():
            OID = sortie.split('\n')
            for i, ligne in enumerate(OID):
                OID[i] = ligne[:-1]

            manager_data.new_equip_data(nom, adresse_ip, OID)
            msg_add_equipement = "équipement enregistré"
            logging.info("INFO: Equipement " + nom + " ; " + adresse_ip + " enregistré")
        else:
            manager_data.new_equip_data_vierge(nom, adresse_ip)
            msg_add_equipement = "l'équipement est introuvable"
            logging.info("INFO: Equipement " + nom + " ; " + adresse_ip + " non trouvé")
    else:
        manager_data.new_equip_data_vierge(nom, adresse_ip)
        msg_add_equipement = "Le Controlleur est désactivé"

    session['msgAddEquipement'] = msg_add_equipement  # Enregistrez le message dans la session
    manager.add_equipment(nom, adresse_ip, port, communaute)
    return redirect(url_for('index'))

####### Partie ajout équipement SNMP V3
@app.route('/add_equipmentv3', methods=['POST'])
def add_equipmentv3():
    print("ajout equipemenn snmp v3")
    nom = request.form['nom']
    adresse_ip = request.form['adresse_ip']
    username = request.form['username']
    auth_protocol = request.form['auth_protocol']
    auth_password = request.form['auth_password']
    privacy_protocol = request.form['privacy_protocol']
    privacy_password = request.form['privacy_password']

    #----------execution du code pour vérification--------------------------
    if etat_SNMP==True:
        commande = './multi_SNMP_v3.sh ' + adresse_ip + ' ' + username + ' ' + auth_protocol + ' ' + auth_password + ' ' + privacy_protocol + ' ' + privacy_password
        process = subprocess.Popen(commande, shell=True, stdout=subprocess.PIPE)
        sortie = process.stdout.read().decode()

        if sortie.strip():
            msg_add_equipement = "équipement enregistré"
            OID = sortie.split('\n')
            for i, ligne in enumerate(OID):
                OID[i] = ligne[:-1]

            manager_data.new_equip_data(nom, adresse_ip, OID)
        else:
            msg_add_equipement = "l'équipement est introuvable"
            manager_data.new_equip_data_vierge(nom, adresse_ip)
    else:
        msg_add_equipement = "Le Controlleur est désactivé"
        manager_data.new_equip_data_vierge(nom, adresse_ip)

    session['msgAddEquipement'] = msg_add_equipement  # Enregistrez le message dans la session
    manager.add_equipment_v3(nom, adresse_ip, username, auth_protocol, auth_password, privacy_protocol, privacy_password)
    return redirect(url_for('index'))

@app.route('/remove_equipment', methods=['POST'])
def remove_equipment():
    nom = request.form['nom']
    adresse_ip = request.form['adresse_ip']
    manager.remove_equipment(nom, adresse_ip)
    manager_data.remove_equipment(nom, adresse_ip)
    return redirect(url_for('liste_equipements'))
##     code pour modifier un equipement
@app.route('/edit_equipment', methods=['POST'])
def edit_equipment():
    nom = request.form['nom']
    adresse_ip = request.form['adresse_ip']
    new_port = request.form['new_port']  # Le nouveau port que vous souhaitez attribuer à l'équipement
    new_communaute = request.form['new_communaute']  # La nouvelle communauté que vous souhaitez attribuer à l'équipement

    # Effectuez les modifications nécessaires dans la gestion de votre équipement, par exemple, en utilisant votre `manager`.

    # Une fois les modifications effectuées, vous pouvez rediriger l'utilisateur vers la page d'accueil ou une autre page appropriée.
    return redirect(url_for('index'))


#----------------------- Partie 2 ------------------

app.secret_key = 'user'  # Clé secrète pour la gestion des sessions

users_data = load_users_data()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérifiez si le nom d'utilisateur existe dans les données utilisateur
        if username in users_data:
            # Récupérez le mot de passe haché de l'utilisateur
            stored_password = users_data[username]['password']

            # Vérifiez si le mot de passe saisi correspond au mot de passe haché
            if check_password_hash(stored_password, password):
                # Informations d'identification correctes, autorisez l'utilisateur
                session['logged_in'] = True
                logging.info(f"L'utilisateur {username} s'est connecté avec succès.")
                return redirect(url_for('index'))

        # Informations d'identification incorrectes
        msg_alert = "Informations d'identification incorrectes. Veuillez réessayer."
        return render_template('auth.html', msgAlert=msg_alert)

    return render_template('auth.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

#----------------------------- Partie 3 --------------
@app.route('/get_equipment_info', methods=['POST'])
def get_equipment_info():
    selected_ip = request.form['selected_equipment']
    selected_equipment = None
    selected_data = None

    # Recherchez l'équipement en fonction de l'adresse IP sélectionnée
    for equipment in manager.get_equipment_list():
        if equipment['AdresseIP'] == selected_ip:
            selected_equipment = equipment
            break

    for data in manager_data.get_equipment_list():
        if data['AdresseIP'] == selected_ip:
            selected_data = data
            break

    # Récupérer les données de "traffic" depuis votre fichier JSON
    traffic_data = selected_data['traffic']
    

    # Créer une liste d'étiquettes (par exemple, les indices des enregistrements)
    labels = [str(i) for i in range(1, len(traffic_data) + 1)]
    print(f"{labels}")

    if selected_equipment:
        # Affichez les informations de l'équipement (par exemple, dans un modèle séparé)
        return render_template('equipment_info.html', equipment=selected_equipment, data_equipment=selected_data, traffic_labels=labels, traffic_data=traffic_data)
    else:
        return "Équipement introuvable."



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password = generate_password_hash(password)
        # Créez un nouvel utilisateur
        new_user = {
            'username': username,
            'password': hashed_password,  # Vous devrez hacher le mot de passe pour des raisons de sécurité
            'email': email
        }

        # Ajoutez l'utilisateur à votre variable users_data
        users_data[username] = new_user

        # Enregistrez les modifications dans le fichier JSON
        with open('users.json', 'w') as f:
            json.dump(users_data, f)

        # Redirigez l'utilisateur vers une page de confirmation ou de connexion
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/voir_logs')
def voir_logs():
    log_lines =  []

    with open('app.log', 'r', encoding='ISO-8859-1') as log_file:
        # log = log_file.read()

        # Lire les dernières lignes du fichier (par exemple, 100 lignes)
        log_lines = log_file.readlines()[-100:]

    return render_template('logs.html', logs=log_lines)

@app.route('/download_logs')
def download_logs():
    # Le chemin complet vers votre fichier de logs
    log_file_path = 'app.log'

    # Nom du fichier de téléchargement
    download_filename = 'logs.txt'

    return send_file(log_file_path, as_attachment=True, download_name=download_filename)

############ affichage de la liste des equipemnts
@app.route('/liste_equipements')
def liste_equipements():
    # Chargez la liste des équipements depuis le fichier de stockage
    equipment_list = manager.get_equipment_list()

    return render_template('liste_equipements.html', equipment_list=equipment_list)

############ affichage de la page erreur 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html'), 500

logging.info("Ceci est un message de journalisation d'information.")



if __name__ == "__main__":
    from threading import Thread
    Thread(target=job).start()

    from waitress import serve
    serve(app, host="0.0.0.0", port=9000)
