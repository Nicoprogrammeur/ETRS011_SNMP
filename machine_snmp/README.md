## Lancement d'un contenaire SNMP pour des test

Simulation d'un équipement SNMP

lancer le conteneur: <br>
`docker build -t simple-snmp .` <br>
`docker run -p 161:161/udp --name snmp-container simple-snmp` <br>
