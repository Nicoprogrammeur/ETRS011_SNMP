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

    def save_equipment_list(self):
        equipment_info = {'equipements': self.equipment_list}
        with open(self.filename, 'w') as file:
            json.dump(equipment_info, file, indent=4)

    def add_equipment(self, nom, adresse_ip, port, community):
        for equipement in self.equipment_list:
            if equipement['Nom'] == nom and equipement['AdresseIP'] == adresse_ip:
                print(f"L'équipement '{nom}' avec l'adresse IP '{adresse_ip}' existe déjà.")
                return
        new_equipment = {'Nom': nom, 'AdresseIP': adresse_ip, 'port': port, 'community': community}
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


