# Projet Supervision SNMP

## Introduction

On se propose de développer un système de surveillance de matériel “réseau” à l’aide du protocole SNMP 

Les objectifs principaux de cette application sont de pouvoir : 

- Surveiller en ligne l’ensemble du matériel constituant le parc. Cette surveillance pourra avoir une représentation textuelle et graphique. 

- Sauvegarder (en fichier ou base de données) l’ensemble des données issues du matériel. 

- Gérer les défaillances matérielles (message d’erreur) en les reportant sur les interfaces “utilisateur” ainsi que dans les systèmes de “log”  

**Dans le cadre de ce développement, on souhaite tout d’abord se focaliser sur la surveillance du nombre d’octets traversant une interface réseau et afficher sous forme de graphe l’ensemble des données obtenues**

## Lancement de l'Application

L'ensemble de l'application son des programmes Python qui tourne sur un Docker <br>
Verifiez que vous possedez Docker, et que ce dernier soit activé sur votre espace de travail <br>

Commencer à télécharger le contenue entier du dépot git: <br>
`$ git clone https://github.com/Nicoprogrammeur/ETRS011_SNMP.git` <br>

Ensuite, à l'aide d'un terminal, lancer le conteneur: <br>
`$ docker build -t snmp_app .` <br>
`$ docker run -p 9000:9000 snmp_app` <br>
> Si vous avez Docker Desktop, vous pouvez l'utiliser pour lancer le conteneur

Le serveur web se lancera tout seul après le démarrage du conteneur <br>

Et connectez vous sur un navigateur:<br>
`http://127.0.0.1:9000`<br>
ou
`http://localhost:9000`<br>
ou
`http://<votre_adresse_IP>:9000`<br>

Sur cette page web, Connectez un utilisateur par exemple `root` avec le mot de passe `root`,<br>
Vous pourrez ensuite ajouter des équipements avec SNMP, puis lancer la supervision en appuyent sur le bouton `Play Controlleur`,<br>
Sur la page `Liste des équipements`, on voit tout les équipements ajouté grâce au formulaire<br>
> La supervision sera lancer quand ce bouton sera rouge<br>

Dans l'état actuel, le programme va tourner en boucle toutes les minutes pour récupérer les données de tous les équipements ajouté sur la page web<br>
> Laissez la supervision tourner un peu pour actualiser les différentes donnéessur la page web<br>

## Contenaire de test

Pour savoir si le contenaire principale fonctionne, nous avons mis en place un second contenaire qui va simuler le comportement d'un équipements SNMP<br>
Il est disponible dans le répertoire du dépot `machine_snmp`

`$ cd machine_snmp`

Et ensuite on démarre ce contenaire :<br>
`$ docker build -t simple-snmp .` <br>
`$ docker run -p 161:161/udp --name snmp-container simple-snmp` <br>
> Il faut que ce contenaire soit démarrer après le principale

<br>

Si tout ces bien passer, le second contenaire devrait avoir comme adresse IP : `172.17.0.3`
> `172.17.0.1` est celle de votre machine ; `172.17.0.2` l'application (le contenaire principale) <br>

> Si c'est pas le cas, utilisé la commande pour afficher son adresse IP : <br> `$ docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snmp-container`

Ce docker va simuler une machine SNMP en version 2c avec comme community `public`