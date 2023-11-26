# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 14:11:36 2023

@author: user
"""

import json

class EquipmentManager:
    def __init__(self, filename):
        self.filename = filename
        self.equipment_list = self.load_equipment_list()

    def load_equipment_list(self):
        try:
            with open(self.filename, 'r') as file:
                equipment_info = json.load(file)
                return equipment_info.get('equipements', [])
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError as e:
            print(f"Error loading equipment list: {e}")
            return []

    def save_equipment_list(self):
        equipment_info = {'equipements': self.equipment_list}
        with open(self.filename, 'w') as file:
            json.dump(equipment_info, file, indent=4)


    def add_equipment(self, nom, adresse_ip, port, community):
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                print(f"L'équipement '{nom}' avec l'adresse IP '{adresse_ip}' existe déjà.")
                return
        new_equipment = {
            'Nom': nom,
            'AdresseIP': adresse_ip,
            'SNMP': 'v2c',
            'port': port,
            'community': community
            }
        self.equipment_list.append(new_equipment)
        self.save_equipment_list()

    #### Partie ajout d'un équipement SNMP V3
    def add_equipment_v3(self, nom, adresse_ip, username, auth_protocol, auth_password, privacy_protocol, privacy_password):
        print("ajout equipement snmp v3 dans le json")
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                print(f"L'équipement '{nom}' avec l'adresse IP '{adresse_ip}' existe déjà.")
                return
        new_equipment = {
            'Nom': nom,
            'AdresseIP': adresse_ip,
            'SNMP': 'v3',
            'Username': username,
            'AuthProtocol': auth_protocol,
            'AuthPassword': auth_password,
            'PrivacyProtocol': privacy_protocol,
            'PrivacyPassword': privacy_password
            }
        self.equipment_list.append(new_equipment)
        self.save_equipment_list()

    def new_equip_data(self, nom, adresse_ip, oid):
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                print(f"L'équipement '{nom}' avec l'adresse IP '{adresse_ip}' existe déjà.")
                return
        new_equipment = {
            'Nom': nom,
            'AdresseIP': adresse_ip,
            'OID': {
                "ipAdEntAddr": oid[0],
                "sysName": oid[1],
                "sysContact": oid[2],
                "sysDescr": oid[3],
                "sysLocation": oid[4],
                "sysUpTime": oid[5],
                "IfHCInOctets": oid[6],
                "IfHCOutOctets": oid[7]
                },
            "traffic": [
               {"in": oid[6], "out": oid[7]}
            ]
        }
        self.equipment_list.append(new_equipment)
        self.save_equipment_list()

    def remove_equipment(self, nom, adresse_ip):
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                self.equipment_list.remove(equipement)
                self.save_equipment_list()
                return

    def get_equipment_list(self):
        return self.equipment_list

    def update_equipment(self, nom, adresse_ip, new_port, new_community):
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                equipement['port'] = new_port
                equipement['community'] = new_community
                self.save_equipment_list()
                return

    def add_data_equip(self, nom, adresse_ip, oid):
        # Charger le contenu du fichier JSON existant
        with open(self.filename, 'r') as file:
            equipements_data = json.load(file)

        # Modifier les données en mémoire
        for equipement in equipements_data.get('equipements', []):
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                # Ajouter les données que vous recevez, par exemple :
                equipement['OID']['ipAdEntAddr'] = oid[0]
                equipement['OID']['sysName'] = oid[1]
                equipement['OID']['sysContact'] = oid[2]
                equipement['OID']['sysDescr'] = oid[3]
                equipement['OID']['sysLocation'] = oid[4]
                equipement['OID']['sysUpTime'] = oid[5]
                equipement['OID']['IfHCInOctets'] = oid[6]
                equipement['OID']['IfHCOutOctets'] = oid[7]

                new_data_graph = {
                    'in': oid[6],
                    'out': oid[7]
                }
                equipement['traffic'].append(new_data_graph)

        # Sauvegarder les modifications dans le fichier JSON
        with open(self.filename, 'w') as file:
            json.dump(equipements_data, file, indent=4)  # Utilisez indent=4 pour une meilleure lisibilité du fichier

# Utilisation de la classe EquipmentManager
if __name__ == '__main__':
    manager = EquipmentManager('materiel.json')

    # Ajouter un équipement
    #manager.add_equipment('Equipement1', '192.168.1.1', 80, 'public')

    # Supprimer un équipement
   # manager.remove_equipment('Equipement1', '192.168.1.1')

    # Obtenir la liste des équipements
    equipment_list = manager.get_equipment_list()
    print(equipment_list)
